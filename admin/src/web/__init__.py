from flask import Flask
from flask import render_template
from src.web.controllers.tags import tags_bp
from src.web.handlers import error
from src.web.controllers.advanced_search import advanced_search_bp

def create_app(env='development', static_folder='../../static'):
    app = Flask(__name__, static_folder=static_folder)

    @app.route('/')
    def home():
        return render_template('home.html')

    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(500, error.internal_server_error)

    app.register_blueprint(advanced_search_bp)
    app.register_blueprint(tags_bp)
    return app