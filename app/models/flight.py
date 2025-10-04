from app import db

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(150), nullable=False)
    flight_image = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)