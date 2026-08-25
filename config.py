import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IS_VERCEL = bool(os.environ.get('VERCEL'))

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'autozcrave_studio_dha_lahore_secret_key_2026')
    
    # Database Configuration (SQLite default, ready for PostgreSQL / MySQL via DATABASE_URL env)
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    elif IS_VERCEL:
        # On Vercel serverless, /tmp is the only writable directory
        DATABASE_PATH = '/tmp/autozcrave.db'
        src_db = os.path.join(BASE_DIR, 'database', 'autozcrave.db')
        if not os.path.exists(DATABASE_PATH) and os.path.exists(src_db):
            try:
                shutil.copy2(src_db, DATABASE_PATH)
            except Exception:
                pass
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    else:
        DATABASE_DIR = os.path.join(BASE_DIR, 'database')
        try:
            os.makedirs(DATABASE_DIR, exist_ok=True)
        except OSError:
            pass
        DATABASE_PATH = os.path.join(DATABASE_DIR, 'autozcrave.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 30,
            'check_same_thread': False
        } if not os.environ.get('DATABASE_URL') else {},
        'pool_pre_ping': True,
    }
    
    # Upload Settings
    if IS_VERCEL:
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Business Contact & Branding
    BUSINESS_NAME = "AutozCraveStudio"
    LOCATION = "DHA Phase 8, Lahore, Pakistan"
    PHONE = "+92 302 4577493"
    WHATSAPP_NUMBER = "923024577493"  # Formatted for wa.me links
    EMAIL = "info@autozcravestudio.com"
    ADDRESS = "Autozcravestudio 75B Green Avenue, Near Broadway Commercial, DHA Phase 8, Lahore, Pakistan"
    WORKING_HOURS = "Mon - Sat: 10:00 AM - 08:00 PM"
