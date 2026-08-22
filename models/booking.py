from datetime import datetime
import random
import string
from models import db

def generate_booking_ref():
    chars = string.ascii_uppercase + string.digits
    rand_str = ''.join(random.choices(chars, k=6))
    return f"AZC-{rand_str}"

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    reference_code = db.Column(db.String(20), unique=True, nullable=False, default=generate_booking_ref, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    vehicle_make = db.Column(db.String(50), nullable=False)
    vehicle_model = db.Column(db.String(50), nullable=False)
    vehicle_year = db.Column(db.String(10), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    preferred_date = db.Column(db.String(20), nullable=False)
    preferred_time = db.Column(db.String(20), nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.reference_code} - {self.customer_name}>'
