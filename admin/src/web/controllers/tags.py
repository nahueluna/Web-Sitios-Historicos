from flask import Blueprint, render_template, request, Response, redirect, flash, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.models.search import create_tag, list_tags, update_tag_name, get_tag_by_id, remove_tag, tag_has_association_with_site
from src.web.controllers.helpers.tags import verify_tag_and_generate_slug, handle_db_error

tags_bp = Blueprint('tags', __name__, url_prefix='/etiquetas')

@tags_bp.get('/')
def view_tags():
    order_by = request.args.get('order_by', 'inserted_at')
    order_dir = request.args.get('order_dir', 'asc')
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 25

    try:
        tags_list, total = list_tags(order_by, order_dir, query, page=page, per_page=per_page)
    except (ValueError, SQLAlchemyError) as e:
        return handle_db_error(
            e,
            "Error getting tags",
            "Ocurrió un error al obtener las etiquetas. Por favor, intente nuevamente.",
            "tags/index.html",
            tags=[]
        )

    return render_template('tags/index.html', tags=tags_list, page=page, total=total, per_page=per_page)

@tags_bp.get('/agregar')
def show_add_tag_form():
    return render_template('tags/add_tag.html')

@tags_bp.post('/agregar')
def add_tag():
    tag_name = request.form.get('name')
    slug_reponse = verify_tag_and_generate_slug(tag_name)

    if isinstance(slug_reponse, Response) and (slug_reponse.status_code == 400):
        flash("El nombre de la etiqueta es obligatorio y debe contener entre 3 y 50 caracteres.", "danger")
        return render_template('tags/add_tag.html')

    try:
        create_tag(name=tag_name, slug=slug_reponse)
    except IntegrityError as e:
        return handle_db_error(
            e,
            "Error creating tag",
            "El nombre de la etiqueta ya existe. Por favor, elija otro.",
            "tags/add_tag.html"
        )
    except SQLAlchemyError as e:
        return handle_db_error(
            e,
            "Error creating tag",
            "Ocurrió un error al crear la etiqueta. Por favor, intente nuevamente.",
            "tags/add_tag.html"
        )

    flash("Etiqueta creada exitosamente.", "success")
    return redirect("/etiquetas/")

@tags_bp.post('/eliminar/<int:tag_id>')
def delete_tag(tag_id):
    print(request.form.get('_method'))
    if request.form.get('_method') == "DELETE":

        if tag_has_association_with_site(tag_id):
            flash("No se puede eliminar la etiqueta porque está asociada a uno o más sitios históricos.", "warning")
            return redirect("/etiquetas/")

        if remove_tag(tag_id):
            flash("Etiqueta eliminada exitosamente.", "success")
        else:
            flash("Ocurrió un error al intentar eliminar la etiqueta.", "danger")

        return redirect("/etiquetas/")
    else:
        abort(405)

@tags_bp.get('/actualizar/<int:tag_id>')
def show_update_tag_form(tag_id):
    tag = get_tag_by_id(tag_id)

    if tag is None:
        return redirect("/etiquetas/")

    return render_template('tags/edit_tag.html', tag_id=tag_id, tag_name=tag.name)

@tags_bp.post('/actualizar/<int:tag_id>')
def update_tag(tag_id):
    if request.form.get('_method') == "PUT":
        new_name = request.form.get('name')
        previous_name = request.form.get('original_name')

        slug_reponse = verify_tag_and_generate_slug(new_name)

        if isinstance(slug_reponse, Response) and (slug_reponse.status_code == 400):
            flash("El nombre de la etiqueta es obligatorio y debe contener entre 3 y 50 caracteres.", "danger")
            return render_template('tags/edit_tag.html', tag_id=tag_id, tag_name=previous_name)

        try:
            update_tag_name(tag_id, new_name, slug_reponse)
        except IntegrityError as e:
            return handle_db_error(
                e,
                "Error updating tag: ",
                "El nombre de la etiqueta ya existe. Por favor, elija otro.",
                "tags/edit_tag.html",
                tag_id=tag_id,
                tag_name=previous_name
            )
        except SQLAlchemyError as e:
            return handle_db_error(
                e,
                "Error updating tag: ",
                "Ocurrió un error al actualizar la etiqueta. Por favor, intente nuevamente.",
                "tags/edit_tag.html",
                tag_id=tag_id,
                tag_name=previous_name
            )

        flash("Etiqueta actualizada exitosamente.", "success")
        return redirect("/etiquetas/")
    else:
        abort(405)