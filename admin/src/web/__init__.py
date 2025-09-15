from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.web.controllers.historic_sites import historyc_sites_bp

def create_app(env='development', static_folder='../../static'):
    app = Flask(__name__, static_folder=static_folder)

    app.register_blueprint(historyc_sites_bp) 

    @app.route('/')
    def home():
        return render_template('home.html')

    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(500, error.internal_server_error)

    return app