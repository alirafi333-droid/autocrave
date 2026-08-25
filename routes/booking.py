from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from models.service import Service
from models.booking import Booking

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        vehicle_make = request.form.get('vehicle_make', '').strip()
        vehicle_model = request.form.get('vehicle_model', '').strip()
        vehicle_year = request.form.get('vehicle_year', '').strip()
        service_id = request.form.get('service_id')
        preferred_date = request.form.get('preferred_date', '').strip()
        preferred_time = request.form.get('preferred_time', '').strip()
        additional_notes = request.form.get('additional_notes', '').strip()

        # Validation
        if not all([customer_name, customer_email, customer_phone, vehicle_make, vehicle_model, vehicle_year, service_id, preferred_date, preferred_time]):
            flash('Please complete all required fields in the booking form.', 'error')
            return redirect(url_for('booking.book', service_id=service_id))

        service = Service.query.get(service_id)
        if not service or not service.is_active:
            flash('Selected service is invalid or unavailable.', 'error')
            return redirect(url_for('booking.book'))

        try:
            new_booking = Booking(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                vehicle_make=vehicle_make,
                vehicle_model=vehicle_model,
                vehicle_year=vehicle_year,
                service_id=service.id,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                additional_notes=additional_notes,
                status='Pending'
            )

            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for('booking.confirmation', reference_code=new_booking.reference_code))
        except Exception as e:
            db.session.rollback()
            flash('A server error occurred while processing your booking. Please try again.', 'error')
            return redirect(url_for('booking.book', service_id=service_id))

    # GET Request
    selected_service_id = request.args.get('service_id', type=int)
    services = Service.query.filter_by(is_active=True).all()
    return render_template('booking.html', services=services, selected_service_id=selected_service_id)

@booking_bp.route('/booking/confirmation/<reference_code>')
def confirmation(reference_code):
    booking = Booking.query.filter_by(reference_code=reference_code).first_or_404()
    return render_template('booking_confirmation.html', booking=booking)
