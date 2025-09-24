from flask import Blueprint, render_template, request, Response, redirect
from sqlalchemy.exc import IntegrityError

from src.core.search import create_tag, list_tags_by_insertion_date
from src.web.controllers.helpers.tags import verify_tag_and_generate_slug

tags_bp = Blueprint('tags', __name__, url_prefix='/etiquetas')

@tags_bp.get('/')
def view_tags():
    tags_list = list_tags_by_insertion_date()
    return render_template('tags/index.html', tags=tags_list)


@tags_bp.get('/agregar')
def show_add_tag_form():
    return render_template('tags/add_tag.html')

@tags_bp.post('/agregar')
def add_tag():
    tag_name = request.form.get('name')
    slug_reponse = verify_tag_and_generate_slug(tag_name)

    if isinstance(slug_reponse, Response):
        return render_template('tags/add_tag.html', bad_request=slug_reponse)

    try:
        create_tag(name=tag_name, slug=slug_reponse)
    except IntegrityError as integrity_error:
        return render_template('tags/add_tag.html', integrity_error=integrity_error)

    return redirect("/search/")

@tags_bp.delete('/eliminar')
def delete_tag(tag_id):
    tag_id = request.args.get('id')
    # AQUÍ SE DEBE ELIMINAR DE LA BASE DE DATOS
    return f"Etiqueta con ID {tag_id} eliminada exitosamente."

@tags_bp.post('/actualizar')
def update_tag():
    tag_id = request.form.get('id')
    new_name = request.form.get('name')

    if not tag_id or not new_name:
        return Response("El ingreso de un nombre para el tag es obligatorio.", status=400)
    if not (3 <= len(new_name) <= 50):
        return Response("El nombre de la etiqueta debe tener entre 3 y 50 caracteres.", status=400)

    new_slug = new_name.lower().replace(' ', '-')
    # AQUÍ SE DEBE ACTUALIZAR EN LA BASE DE DATOS

    return f"Etiqueta actualizada exitosamente a '{new_name}'."