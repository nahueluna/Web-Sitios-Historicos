from datetime import datetime

from flask import Blueprint, render_template, request, Response, redirect, flash, abort, jsonify, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.models.review import get_specific_review, update_review_status
from src.core.models.auth import get_usuario_by_email
from src.core.models.review.review import ReviewStatus
from src.web.decorator import block_admin_maintenance

from src.core.models.review import list_reviews_with_filters
from src.web.controllers.helpers.tags import verify_tag_and_generate_slug, handle_db_error
from src.web.handlers.auth import role_required
from src.core.models.auth.user import RolUsuario
from src.web.controllers.helpers.time import date_is_greater_than

review_bp = Blueprint('review', __name__, url_prefix='/admin/reviews')

@review_bp.get('/')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def index_redirect(_user):
    return redirect(url_for('review.render_index'))

@review_bp.get('/explore')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_index(_user):
    return render_template(
        'review/index.html',
        ReviewStatus=ReviewStatus,
    )

@review_bp.get('/search')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def get_reviews(_user):
    params = request.args.to_dict()
    per_page = 25

    try:
        rating = params.get('rating', None)

        if rating:
            if not (1 <= int(rating) <= 5):
                return jsonify({"error": "Invalid rating"}), 400

        date_from = params.get('date_from', None)
        date_to = params.get('date_to', None)

        if date_from and date_to:
            if date_is_greater_than(date_from, date_to):
                return jsonify({"error": "date_from cannot be greater than date_to"}), 400

        status = params.get('status', None)
        if status:
            if status not in ReviewStatus.__members__:
                return jsonify({"error": "Invalid status"}), 400

        params['per_page'] = str(per_page)

        page = params.pop('page', '1')
        params['page'] = page

    except:
        return jsonify({"error": "An error has occurred while applying the filters"}), 500

    try:
        (reviews, total) = list_reviews_with_filters(**params)
        json = [r.json() for r in reviews]

        json_data = {
            "reviews": json,
            "total": total,
            "per_page": per_page,
            "page": int(page),
        }

        return jsonify(json_data), 200
    except (ValueError, SQLAlchemyError) as e:
        return handle_db_error(
            e,
            "Error getting reviews",
            "Ocurrió un error al obtener las reseñas. Por favor, intente nuevamente.",
            "review/index.html",
            ReviewStatus=ReviewStatus
        )

@review_bp.post('/approve/<int:review_id>')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def approve_review(_user, review_id):
    if request.form.get('_method') == "PUT":
        review = get_specific_review(review_id)

        if review.status != ReviewStatus.PENDING:
            flash("Solo una reseña pendiente puede aprobarse.", "warning")
            return redirect(url_for('review.render_index'))

        try:
            update_review_status(review_id, new_status=ReviewStatus.APPROVED)
        except SQLAlchemyError as e:
            return handle_db_error(
                e,
                "Error approving review",
                "Ocurrió un error al intentar aprobar la reseña. Por favor, intente nuevamente.",
                "review/index.html",
                ReviewStatus=ReviewStatus
            )

        flash("Reseña aprobada exitosamente.", "success")
        return redirect(url_for('review.render_index'))
    else:
        abort(405)

@review_bp.post('/reject/<int:review_id>')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def reject_review(_user, review_id):
    if request.form.get('_method') == "PUT":
        review = get_specific_review(review_id)
        rejection_reason = request.form.get('rejection-reason', None)

        if review.status != ReviewStatus.PENDING:
            flash("Solo una reseña pendiente puede rechazarse.", "warning")
            return redirect(url_for('review.render_index'))

        if not rejection_reason:
            flash("El motivo de rechazo es obligatorio para rechazar una reseña", "warning")
            return redirect(url_for('review.render_index'))

        try:
            update_review_status(review_id, new_status=ReviewStatus.REJECTED, review_rejection_reason=rejection_reason)
        except SQLAlchemyError as e:
            return handle_db_error(
                e,
                "Error rejecting review",
                "Ocurrió un error al intentar rechazar la reseña. Por favor, intente nuevamente.",
                "review/index.html",
                ReviewStatus=ReviewStatus
            )

        flash("Reseña rechazada exitosamente.", "success")
        return redirect(url_for('review.render_index'))
    else:
        abort(405)