from flask import Flask
from flask import render_template
from flask_session import Session
from src.web.controllers.tags import tags_bp
from src.web.handlers import error
from src.web.handlers.auth import is_authenticated
from src.web.controllers.user_controller import bp_user
from src.web.controllers.advanced_search import advanced_search_bp
from src.web.config import config
from src.core import database
from src.web.controllers.historic_sites import historic_sites_bp
from src.web.controllers.historic_sites import render_index
from src.web.controllers.role_controller import role_bp
from src.web.controllers.user_controller import bp_user
from src.web.controllers.auth import bp_auth
from src.core.bcrypt import bcrypt


session = Session()

def create_app(env='development', static_folder='../../static'):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    database.init_app(app)  # Inicializar la base de datos

    session.init_app(app)

    bcrypt.init_app(app)

    app.register_blueprint(historic_sites_bp)

    @app.route('/')
    def home():  # return render_index()
        return render_template('home.html')

    @app.route('/admin')
    def admin():
        return render_template('layout.html')

    @app.route('/admin/validacion-propuestas')
    def validacion_propuestas():
        return render_template('validacion_propuestas.html')

    @app.route('/admin/moderacion')
    def moderacion():
        return render_template('moderacion.html')

    @app.route('/admin/gestion-usuarios')
    def gestion_usuarios():
        return render_template('gestion_usuarios.html')

    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(500, error.internal_server_error)
    app.register_error_handler(405, error.method_not_allowed)

    # Registrar funcion global
    app.jinja_env.globals['is_authenticated'] = is_authenticated

    app.register_blueprint(advanced_search_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(bp_user)
    app.register_blueprint(role_bp)
    app.register_blueprint(bp_auth)

    @app.cli.command("reset-db")
    def reset_db():
        database.reset_db()

    @app.cli.command("seed-db-user")
    def seed_db_user():
        database.seed_db_user()

    @app.cli.command("seed-db")
    def seed_db():
        database.seed_db()

    return app
