from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from models.service import Service
from models.gallery import GalleryItem
from models.contact import ContactMessage

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    services = Service.query.filter_by(is_active=True).limit(6).all()
    gallery_items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).limit(6).all()
    return render_template('index.html',
                           services=services,
                           gallery_items=gallery_items)

@main_bp.route('/services')
def services():
    services_list = Service.query.filter_by(is_active=True).all()
    return render_template('services.html', services=services_list)

@main_bp.route('/products-used')
def products_used():
    return render_template('products_used.html')

@main_bp.route('/instagram-work')
def instagram_work():
    return render_template('instagram_work.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not subject or not message:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('main.contact'))

        new_msg = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()

        flash('Thank you! Your message has been sent successfully. We will get back to you shortly.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html')
