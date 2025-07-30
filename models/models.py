from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

# table user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
# ParkingLot table
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)

    def __init__(self, prime_location_name, address, pin_code, price, maximum_number_of_spots):
        self.prime_location_name = prime_location_name
        self.address = address
        self.pin_code = pin_code
        self.price = price
        self.maximum_number_of_spots = maximum_number_of_spots

# ParkingSpot table
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    spot_number = db.Column(db.String(20), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)

    def __init__(self, lot_id, spot_number, is_occupied=False):
        self.lot_id = lot_id
        self.spot_number = spot_number
        self.is_occupied = is_occupied
# Reservation table
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    vehicle_no = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='parked')
    releasing_time = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, nullable=True)

    def __init__(self, user_id, spot_id, vehicle_no, status='parked'):
        self.user_id = user_id
        self.spot_id = spot_id
        self.vehicle_no = vehicle_no
        self.status = status
    def calculate_total_cost(self):
        lot_price_per_unit_time = self.lot.price
        time_diff = (self.releasing_time - self.timestamp).total_seconds() / 3600
        total_cost = lot_price_per_unit_time * time_diff
        return total_cost


