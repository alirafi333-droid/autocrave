from datetime import datetime
from models import db

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=True)  # e.g., "PKR 45,000" or "Starting PKR 30,000"
    duration = db.Column(db.String(50), nullable=True)  # e.g., "1 - 2 Days"
    image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to bookings
    bookings = db.relationship('Booking', backref='service', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Service {self.name}>'
