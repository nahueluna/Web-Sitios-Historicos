from flask import Flask
from flask import render_template, redirect, url_for
from flask_session import Session
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from src.web.controllers.tags import tags_bp
from src.web.handlers import error
from src.web.handlers.auth import is_authenticated, is_system_admin, is_admin, is_editor_or_admin
from src.web.controllers.user_controller import bp_user
from src.web.config import config
from src.core import database
from src.web.controllers.historic_sites import historic_sites_bp
from src.web.controllers.historic_sites import render_index
from src.web.controllers.role_permission import role_bp
from src.web.controllers.user_controller import bp_user
from src.web.controllers.google_login import bp_google_auth
import src.web.controllers.advanced_search
from src.web.controllers.review import review_bp
from src.web.controllers.auth import bp_auth
from src.web.controllers.feature_flag import feature_flag_bp
from src.web.api.sites import sites_api
from src.web.api.reviews import reviews_api
from src.web.api.auth import auth_api
from src.web.api.favorites import favorites_api
from src.web.api.tags import tags_api
from src.core.bcrypt import bcrypt
from flask_cors import CORS
from src.web.storage import storage


session = Session()
jwt = JWTManager()

def create_app(env='development', static_folder='../../static'):
    load_dotenv()
    
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    database.init_app(app)  # Inicializar la base de datos

    session.init_app(app)

    bcrypt.init_app(app)

    jwt.init_app(app)

    ## Necesario para el OAuth2 con Google
    CORS(
        app, 
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        origins=["http://localhost:5173",  "http://127.0.0.1:5173", "https://admin-grupo03.proyecto2025.linti.unlp.edu.ar", "https://grupo03.proyecto2025.linti.unlp.edu.ar"], 
        supports_credentials=True)  # URL de tu frontend Vue
    app.secret_key = app.config["SECRET_KEY"]
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    # Inicializar Storage
    storage.init_app(app)


    @app.route('/')
    def home():  # return render_index()
        if is_authenticated():
            return render_template('home.html')
        else:
            return redirect(url_for("auth.login"))

    #@app.route('/admin')
    #def admin():
    #    return render_template('layout.html')

    #@app.route('/admin/validacion-propuestas')
    #def validacion_propuestas():
    #    return render_template('validacion_propuestas.html')

    #@app.route('/admin/moderacion')
    #def moderacion():
    #    return render_template('moderacion.html')

    #@app.route('/admin/gestion-usuarios')
    #def gestion_usuarios():
    #    return render_template('gestion_usuarios.html')

    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(500, error.internal_server_error)
    app.register_error_handler(405, error.method_not_allowed)

    # Registrar funciones globales para templates
    app.jinja_env.globals['is_authenticated'] = is_authenticated
    app.jinja_env.globals['is_system_admin'] = is_system_admin

    ## Funciones globales que usa juani
    app.jinja_env.globals['is_admin'] = is_admin
    app.jinja_env.globals['is_editor_or_admin'] = is_editor_or_admin

    app.register_blueprint(historic_sites_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(bp_user)
    app.register_blueprint(role_bp)
    app.register_blueprint(bp_auth)
    app.register_blueprint(feature_flag_bp)
 
    app.register_blueprint(reviews_api)
    app.register_blueprint(sites_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(favorites_api)
    app.register_blueprint(tags_api)
    
    app.register_blueprint(bp_google_auth)
    app.register_blueprint(review_bp)

    @app.cli.command("reset-db")
    def reset_db():
        database.reset_db()

    @app.cli.command("seed-db-user")
    def seed_db_user():
        database.seed_db_user()

    @app.cli.command("seed-db")
    def seed_db():
        database.seed_db()

    @app.cli.command("seed-images")
    def seed_images():
        database.seed_db_images()

    return app
