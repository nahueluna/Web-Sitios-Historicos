from flask import Flask
from flask import render_template
from src.web.controllers.tags import tags_bp
from src.web.handlers import error
from src.web.controllers.user_controller import bp_user
from src.web.controllers.advanced_search import advanced_search_bp
from src.web.config import config
from src.core import database

def create_app(env='development', static_folder='../../static'):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    database.init_app(app)  # Inicializar la base de datos

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/admin')
    def admin():
        return render_template('layout.html')

    @app.route('/admin/gestion-sitios')
    def gestion_sitios():
        return render_template('gestion_sitios.html')

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

    app.register_blueprint(advanced_search_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(bp_user)

    @app.cli.command("reset-db")
    def reset_db():
        database.reset_db()

    return app
