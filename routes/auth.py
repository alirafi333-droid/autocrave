from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        login_id = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Find by email, name, or special admin ID
        user = User.query.filter(
            (User.email == login_id) | 
            (User.name == login_id) |
            (User.email == f"{login_id}@autozcrave.com")
        ).first()

        if user and user.check_password(password):
            if not user.is_admin():
                flash('Access denied. Administrator privileges required.', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(user)
            flash('Welcome back! Admin authentication successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid Admin ID/Email or password. Please try again.', 'error')

    return render_template('admin/login.html')

@auth_bp.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))
