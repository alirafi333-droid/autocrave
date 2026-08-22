import os
import uuid
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db
from models.user import User
from models.service import Service
from models.booking import Booking
from models.gallery import GalleryItem
from models.before_after import BeforeAfterItem
from models.contact import ContactMessage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Admin authorization required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file_obj, subfolder=''):
    if not file_obj or file_obj.filename == '':
        return None
    if file_obj and allowed_file(file_obj.filename):
        ext = file_obj.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}.{ext}"
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, filename)
        file_obj.save(filepath)
        # Return web accessible path relative to static
        rel_path = f"uploads/{subfolder}/{filename}" if subfolder else f"uploads/{filename}"
        return rel_path
    return None

# --- DASHBOARD OVERVIEW ---
@admin_bp.route('/')
@admin_required
def dashboard():
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='Pending').count()
    confirmed_bookings = Booking.query.filter_by(status='Confirmed').count()
    completed_bookings = Booking.query.filter_by(status='Completed').count()
    cancelled_bookings = Booking.query.filter_by(status='Cancelled').count()
    
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(status='Unread').count()
    total_gallery = GalleryItem.query.count()
    
    # Calculate unique customers based on email
    unique_customers = db.session.query(Booking.customer_email).distinct().count()
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(8).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_bookings=total_bookings,
                           pending_bookings=pending_bookings,
                           confirmed_bookings=confirmed_bookings,
                           completed_bookings=completed_bookings,
                           cancelled_bookings=cancelled_bookings,
                           total_messages=total_messages,
                           unread_messages=unread_messages,
                           total_gallery=total_gallery,
                           unique_customers=unique_customers,
                           recent_bookings=recent_bookings,
                           recent_messages=recent_messages)

# --- BOOKING MANAGEMENT ---
@admin_bp.route('/bookings')
@admin_required
def bookings():
    search_query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    service_filter = request.args.get('service_id', type=int)
    date_filter = request.args.get('date', '').strip()

    query = Booking.query

    if search_query:
        search_fmt = f"%{search_query}%"
        query = query.filter(
            (Booking.reference_code.ilike(search_fmt)) |
            (Booking.customer_name.ilike(search_fmt)) |
            (Booking.customer_email.ilike(search_fmt)) |
            (Booking.customer_phone.ilike(search_fmt)) |
            (Booking.vehicle_make.ilike(search_fmt)) |
            (Booking.vehicle_model.ilike(search_fmt))
        )
    
    if status_filter:
        query = query.filter_by(status=status_filter)

    if service_filter:
        query = query.filter_by(service_id=service_filter)

    if date_filter:
        query = query.filter_by(preferred_date=date_filter)

    bookings_list = query.order_by(Booking.created_at.desc()).all()
    services_list = Service.query.all()

    return render_template('admin/bookings.html',
                           bookings=bookings_list,
                           services=services_list,
                           search_query=search_query,
                           status_filter=status_filter,
                           service_filter=service_filter,
                           date_filter=date_filter)

@admin_bp.route('/bookings/<int:booking_id>/status', methods=['POST'])
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
        booking.status = new_status
        db.session.commit()
        flash(f'Booking #{booking.reference_code} status updated to {new_status}.', 'success')
    else:
        flash('Invalid status supplied.', 'error')
    return redirect(request.referrer or url_for('admin.bookings'))

@admin_bp.route('/bookings/<int:booking_id>/delete', methods=['POST'])
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash(f'Booking #{booking.reference_code} deleted.', 'info')
    return redirect(url_for('admin.bookings'))

# --- SERVICE MANAGEMENT ---
@admin_bp.route('/services', methods=['GET', 'POST'])
@admin_required
def services():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        duration = request.form.get('duration', '').strip()
        is_active = True if request.form.get('is_active') == 'on' else False

        image_file = request.files.get('image')
        image_path = save_uploaded_file(image_file, 'services') or 'images/default_service.jpg'

        if not name or not description:
            flash('Service Name and Description are required.', 'error')
        else:
            new_service = Service(
                name=name,
                description=description,
                price=price,
                duration=duration,
                image=image_path,
                is_active=is_active
            )
            db.session.add(new_service)
            db.session.commit()
            flash(f'Service "{name}" added successfully.', 'success')
            return redirect(url_for('admin.services'))

    services_list = Service.query.order_by(Service.id.desc()).all()
    return render_template('admin/services.html', services=services_list)

@admin_bp.route('/services/<int:service_id>/edit', methods=['POST'])
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    service.name = request.form.get('name', '').strip()
    service.description = request.form.get('description', '').strip()
    service.price = request.form.get('price', '').strip()
    service.duration = request.form.get('duration', '').strip()
    service.is_active = True if request.form.get('is_active') == 'on' else False

    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        new_path = save_uploaded_file(image_file, 'services')
        if new_path:
            service.image = new_path

    db.session.commit()
    flash(f'Service "{service.name}" updated successfully.', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/<int:service_id>/toggle', methods=['POST'])
@admin_required
def toggle_service(service_id):
    service = Service.query.get_or_404(service_id)
    service.is_active = not service.is_active
    db.session.commit()
    state = "activated" if service.is_active else "deactivated"
    flash(f'Service "{service.name}" has been {state}.', 'info')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash(f'Service "{service.name}" deleted successfully.', 'info')
    return redirect(url_for('admin.services'))

# --- GALLERY MANAGEMENT ---
@admin_bp.route('/gallery', methods=['GET', 'POST'])
@admin_required
def gallery():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'General').strip()
        description = request.form.get('description', '').strip()
        image_file = request.files.get('image')

        image_path = save_uploaded_file(image_file, 'gallery')
        if not title or not image_path:
            flash('Title and Image file are required for gallery upload.', 'error')
        else:
            item = GalleryItem(
                title=title,
                category=category,
                description=description,
                image_path=image_path
            )
            db.session.add(item)
            db.session.commit()
            flash('Gallery image uploaded successfully.', 'success')
            return redirect(url_for('admin.gallery'))

    items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    categories = ['Ceramic Coating', 'Glass Coating', 'Graphene Coating', 'PPF', 'Deep Detailing', 'General']
    return render_template('admin/gallery.html', items=items, categories=categories)

@admin_bp.route('/gallery/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_gallery_item(item_id):
    item = GalleryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item removed.', 'info')
    return redirect(url_for('admin.gallery'))

# --- BEFORE & AFTER MANAGEMENT ---
@admin_bp.route('/before-after', methods=['GET', 'POST'])
@admin_required
def before_after():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        service_category = request.form.get('service_category', 'General').strip()
        description = request.form.get('description', '').strip()

        before_file = request.files.get('before_image')
        after_file = request.files.get('after_image')

        before_path = save_uploaded_file(before_file, 'before_after')
        after_path = save_uploaded_file(after_file, 'before_after')

        if not title or not before_path or not after_path:
            flash('Project Title, BEFORE Image, and AFTER Image are required.', 'error')
        else:
            ba_item = BeforeAfterItem(
                title=title,
                service_category=service_category,
                description=description,
                before_image=before_path,
                after_image=after_path
            )
            db.session.add(ba_item)
            db.session.commit()
            flash('Before & After project created successfully.', 'success')
            return redirect(url_for('admin.before_after'))

    projects = BeforeAfterItem.query.order_by(BeforeAfterItem.created_at.desc()).all()
    categories = ['Ceramic Coating', 'Glass Coating', 'Graphene Coating', 'PPF', 'Deep Detailing', 'General']
    return render_template('admin/before_after.html', projects=projects, categories=categories)

@admin_bp.route('/before-after/<int:project_id>/delete', methods=['POST'])
@admin_required
def delete_before_after(project_id):
    project = BeforeAfterItem.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Before & After project deleted.', 'info')
    return redirect(url_for('admin.before_after'))

# --- CONTACT MESSAGES INBOX ---
@admin_bp.route('/messages')
@admin_required
def messages():
    messages_list = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages_list)

@admin_bp.route('/messages/<int:msg_id>/toggle-read', methods=['POST'])
@admin_required
def toggle_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.status = 'Read' if msg.status == 'Unread' else 'Unread'
    db.session.commit()
    flash(f'Message status set to {msg.status}.', 'info')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/<int:msg_id>/delete', methods=['POST'])
@admin_required
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Contact message deleted.', 'info')
    return redirect(url_for('admin.messages'))
