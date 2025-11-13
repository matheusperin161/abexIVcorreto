from src.models.user import db
from datetime import datetime

class BusLocation(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'bus_location'
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, unique=True, nullable=False) # ID do ônibus sendo rastreado
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'bus_id': self.bus_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat()
        }

    def __repr__(self):
        return f"<BusLocation bus_id={self.bus_id} lat={self.latitude} lon={self.longitude}>"

class Route(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(120), unique=True, nullable=False)
    origin_lat = db.Column(db.Float, nullable=False)
    origin_lon = db.Column(db.Float, nullable=False)
    destination_lat = db.Column(db.Float, nullable=False)
    destination_lon = db.Column(db.Float, nullable=False)
    polyline = db.Column(db.Text, nullable=True) # O encoded polyline da Google
    
    def to_dict(self):
        return {
            'id': self.id,
            'route_name': self.route_name,
            'origin': f"{self.origin_lat},{self.origin_lon}",
            'destination': f"{self.destination_lat},{self.destination_lon}",
            'polyline': self.polyline
        }

    def __repr__(self):
        return f"<Route name={self.route_name}>"
