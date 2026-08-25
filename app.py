import os
from flask import Flask
from config import Config
from models import db
from models.user import User
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # SQLite WAL mode and busy timeout listener for concurrency resilience
    with app.app_context():
        try:
            from sqlalchemy import event
            from sqlalchemy.engine import Engine
            import sqlite3

            @event.listens_for(Engine, 'connect')
            def set_sqlite_pragma(dbapi_connection, connection_record):
                if isinstance(dbapi_connection, sqlite3.Connection):
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA journal_mode=WAL")
                    cursor.execute("PRAGMA synchronous=NORMAL")
                    cursor.execute("PRAGMA busy_timeout=30000")
                    cursor.close()
        except Exception:
            pass

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Context Processor for global settings
    @app.context_processor
    def inject_global_settings():
        return dict(
            config=app.config,
            current_year=2026
        )

    # Ensure upload directory exists safely
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'services'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'before_after'), exist_ok=True)
    except OSError:
        pass

    # Register Blueprints
    from routes.main import main_bp
    from routes.booking import booking_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Create tables automatically
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
