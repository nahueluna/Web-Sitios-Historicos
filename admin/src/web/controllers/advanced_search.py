from flask import Blueprint, render_template, request

advanced_search_bp = Blueprint('advanced_search', __name__, url_prefix='/buscar')

@advanced_search_bp.get('/')
def advanced_search():
    # LA BUSQUEDA DEPENDE DE LAS CONSULTAS A LA BASE DE DATOS
    return render_template('advanced_search/index.html')

