from src.main import app
from src.models.user import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Verifica se o usuário admin já existe
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        # Cria o usuário admin
        hashed_password = generate_password_hash('admin_password')
        admin_user = User(
            username='admin', 
            email='admin@abex.com',
            password=hashed_password,
            role='admin',
            card_balance=0.0
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário 'admin' criado com sucesso.")
    else:
        print("Usuário 'admin' já existe.")

    # Popula rotas de exemplo, se não existirem
    from src.models.user import BusRoute, BusLocation
    if BusRoute.query.count() == 0:
        routes = [
            BusRoute(route_number='001', route_name='Centro - Zona Norte', origin='Centro', destination='Zona Norte', fare=4.50),
            BusRoute(route_number='002', route_name='Centro - Zona Sul', origin='Centro', destination='Zona Sul', fare=4.50),
            BusRoute(route_number='003', route_name='Zona Leste - Centro', origin='Zona Leste', destination='Centro', fare=4.50),
            BusRoute(route_number='004', route_name='Zona Oeste - Centro', origin='Zona Oeste', destination='Centro', fare=4.50),
            BusRoute(route_number='005', route_name='Circular Shopping', origin='Terminal Central', destination='Shopping Center', fare=3.50),
        ]
        for route in routes:
            db.session.add(route)
        db.session.commit()
        print("Rotas de ônibus de exemplo criadas.")
    
    if BusLocation.query.count() == 0:
        locations = [
            BusLocation(route_id=1, bus_number='1001', latitude=-23.5505, longitude=-46.6333),
            BusLocation(route_id=1, bus_number='1002', latitude=-23.5515, longitude=-46.6343),
            BusLocation(route_id=2, bus_number='2001', latitude=-23.5525, longitude=-46.6353),
            BusLocation(route_id=2, bus_number='2002', latitude=-23.5535, longitude=-46.6363),
            BusLocation(route_id=3, bus_number='3001', latitude=-23.5545, longitude=-46.6373),
        ]
        for location in locations:
            db.session.add(location)
        db.session.commit()
        print("Localizações de ônibus de exemplo criadas.")
