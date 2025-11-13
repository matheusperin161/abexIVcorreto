from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.bus_location import BusLocation, Route
from src.config import GOOGLE_API_KEY, ROUTE_ORIGIN_LAT, ROUTE_ORIGIN_LON, ROUTE_DEST_LAT, ROUTE_DEST_LON
import requests
from main import socketio

tracking_bp = Blueprint("tracking", __name__)

@tracking_bp.route("/update_location", methods=["POST"])
def update_location():
    data = request.get_json()
    if not data or 'bus_id' not in data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Invalid data"}), 400

    bus_location = BusLocation.query.filter_by(bus_id=data['bus_id']).first()
    if not bus_location:
        bus_location = BusLocation(
            bus_id=data['bus_id'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(bus_location)
    else:
        bus_location.latitude = data['latitude']
        bus_location.longitude = data['longitude']

    db.session.commit()

    # Emitir a atualização da localização para os clientes conectados
    socketio.emit('location_update', bus_location.to_dict(), namespace='/tracking')

    return jsonify({"success": True, "data": bus_location.to_dict()}), 200

@tracking_bp.route("/route/<int:bus_id>", methods=["GET"])
def get_route(bus_id):
    # 1. Tenta buscar a rota no banco de dados (para evitar chamadas repetidas à API do Google)
    # Por simplicidade, vamos usar um ID de rota fixo para o exemplo
    route_name = f"Linha_{bus_id}"
    route_data = Route.query.filter_by(route_name=route_name).first()

    if route_data and route_data.polyline:
        return jsonify({"polyline": route_data.polyline, "cached": True}), 200

    # 2. Se não estiver no cache, busca na Google Directions API
    try:
        # Use as coordenadas de exemplo do config.py
        origin = f"{ROUTE_ORIGIN_LAT},{ROUTE_ORIGIN_LON}"
        destination = f"{ROUTE_DEST_LAT},{ROUTE_DEST_LON}"
        
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "mode": "driving",
            "key": GOOGLE_API_KEY
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['routes']:
            polyline = data['routes'][0]['overview_polyline']['points']
            
            # 3. Armazena no banco de dados para cache (simulação)
            if not route_data:
                route_data = Route(
                    route_name=route_name,
                    origin_lat=ROUTE_ORIGIN_LAT,
                    origin_lon=ROUTE_ORIGIN_LON,
                    destination_lat=ROUTE_DEST_LAT,
                    destination_lon=ROUTE_DEST_LON,
                    polyline=polyline
                )
                db.session.add(route_data)
            else:
                route_data.polyline = polyline
            
            db.session.commit()
            
            return jsonify({"polyline": polyline, "cached": False}), 200
        else:
            return jsonify({"error": "Erro ao buscar rota na Google API", "details": data.get('error_message', data.get('status'))}), 500

    except Exception as e:
        return jsonify({"error": f"Erro interno ao processar rota: {str(e)}"}), 500

    bus_location = BusLocation.query.filter_by(bus_id=data['bus_id']).first()
    if not bus_location:
        bus_location = BusLocation(
            bus_id=data['bus_id'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(bus_location)
    else:
        bus_location.latitude = data['latitude']
        bus_location.longitude = data['longitude']

    db.session.commit()

    # Emitir a atualização da localização para os clientes conectados
    socketio.emit('location_update', bus_location.to_dict(), namespace='/tracking')

    return jsonify({"success": True, "data": bus_location.to_dict()}), 200

@socketio.on('connect', namespace='/tracking')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/tracking')
def handle_disconnect():
    print('Client disconnected')
