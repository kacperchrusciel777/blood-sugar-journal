import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)

    # Konfiguracja
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)  # <== DODANE

    from app.models import User, MoodEntry

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rejestracja blueprintów
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.mood.routes import bp as mood_bp
    app.register_blueprint(mood_bp, url_prefix='/mood')

    return app
