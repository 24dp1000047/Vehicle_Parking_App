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
    def _repr_(self):
        return f'<User {self.email}>'

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def _repr_(self):
        return f'<ParkingLot {self.prime_location_name}>'

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # 'A' for Available, 'O' for Occupied
    spot_number = db.Column(db.String(20))  # Optional: unique identifier for the spot
    # Add more fields as needed

    lot = db.relationship('ParkingLot', backref=db.backref('spots', lazy=True))

    def _repr_(self):
        return f'<ParkingSpot {self.id} - Lot {self.lot_id} - Status {self.status}>'

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost_per_unit = db.Column(db.Float, nullable=False)
    # Add more fields as needed

    spot = db.relationship('ParkingSpot', backref=db.backref('reservations', lazy=True))
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))

    def _repr_(self):
        return f'<Reservation {self.id} - Spot {self.spot_id} - User {self.user_id}>'