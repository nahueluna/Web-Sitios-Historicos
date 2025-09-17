from flask import Blueprint, render_template, request, Response

tags_bp = Blueprint('tags', __name__, url_prefix='/tags')

@tags_bp.get('/')
def tags():
    # SE VISUALIZAN A PARTIR DE CONSULTA A LA BD
    return render_template('tags/index.html')


@tags_bp.get('/agregar')
def show_add_tag_form():
    return render_template('tags/add_tag.html')

@tags_bp.post('/agregar')
def add_tag():
    tag_name = request.form.get('name')

    if not tag_name:
        return Response("El ingreso de un nombre para el tag es obligatorio.", status=400)
    if not (3 <= len(tag_name) <= 50):
        return Response("El nombre de la etiqueta debe tener entre 3 y 50 caracteres.", status=400)

    slug = tag_name.lower().replace(' ', '-')
    # AQUÍ SE DEBE GUARDAR EN LA BASE DE DATOS

    return f"Etiqueta '{tag_name}' agregada exitosamente."

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