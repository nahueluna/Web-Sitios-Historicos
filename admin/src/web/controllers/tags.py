from flask import Blueprint, render_template, request, Response, redirect, flash
from sqlalchemy.exc import IntegrityError

from src.core.search import create_tag, list_tags_by_update_date, update_tag_name, get_tag_by_id, remove_tag
from src.web.controllers.helpers.tags import verify_tag_and_generate_slug

tags_bp = Blueprint('tags', __name__, url_prefix='/etiquetas')

@tags_bp.get('/')
def view_tags():
    tags_list = list_tags_by_update_date()
    return render_template('tags/index.html', tags=tags_list)

@tags_bp.get('/<int:tag_id>')
def view_specific_tag(tag_id):
    tag = get_tag_by_id(tag_id)

    if tag is None:
        return redirect("/etiquetas/")

    return render_template('tags/view_tag.html', tag=tag)

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

    return redirect("/etiquetas/")

@tags_bp.post('/eliminar/<int:tag_id>')
def delete_tag(tag_id):
    if remove_tag(tag_id):
        flash("Etiqueta eliminada exitosamente.", "success")
    else:
        flash("Ocurrió un error al intentar eliminar la etiqueta.", "error")

    return redirect("/etiquetas/")

@tags_bp.get('/actualizar/<int:tag_id>')
def show_update_tag_form(tag_id):
    tag = get_tag_by_id(tag_id)

    if tag is None:
        return redirect("/etiquetas/")

    return render_template('tags/edit_tag.html', tag_id=tag_id, tag_name=tag.name)

@tags_bp.post('/actualizar/<int:tag_id>')
def update_tag(tag_id):
    new_name = request.form.get('name')

    slug_reponse = verify_tag_and_generate_slug(new_name)

    if isinstance(slug_reponse, Response):
        return render_template('tags/edit_tag.html', tag_id=tag_id, bad_request=slug_reponse)

    try:
        update_tag_name(tag_id, new_name, slug_reponse)
    except IntegrityError as integrity_error:
        return render_template('tags/edit_tag.html', tag_id=tag_id , integrity_error=integrity_error)

    return redirect("/etiquetas/")