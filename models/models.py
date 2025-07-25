from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# table user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email ID (Username)
    password = db.Column(db.String(128), nullable=False)            # Password
    fullname = db.Column(db.String(100), nullable=False)            # Fullname
    address = db.Column(db.Text, nullable=False)                    # Address
    pin_code = db.Column(db.String(10), nullable=False)             # Pin Code
    role = db.Column(db.String(50), nullable=False, default='user')

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_number = db.Column(db.Integer, nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)