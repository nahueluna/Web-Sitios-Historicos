# Modelos
from src.core.models.auth.user import RolUsuario
# Handlers y decoradores
from src.web.decorator import block_admin_maintenance
from src.web.handlers.auth import role_required

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from core.models.historic_sites import list_historic_sites_with_filters
from src.web.controllers.historic_sites import historic_sites_bp
from web.controllers.helpers.tags import handle_db_error
from datetime import datetime


@historic_sites_bp.get('/search')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def get_historic_sites(_user):
    params = request.args.to_dict()
    per_page = 25

    try:
        tags = params.pop('tags')
        if tags:
            tags = tags.split(',')
            params['tags'] = tags

        date_from = params.pop('date_from')
        date_to = params.pop('date_to')

        if date_from:
            params['date_from'] = date_from

        if date_to:
            params['date_to'] = date_to

        if date_from and date_to:
            date_from_millis = int(datetime.strptime(date_from, "%Y-%m-%d").timestamp())
            date_to_millis = int(datetime.strptime(date_to, "%Y-%m-%d").timestamp())

            if date_from_millis > date_to_millis:
                return jsonify({"error": "date_from cannot be greater than date_to"}), 400


        params['per_page'] = str(per_page)

        page = params.pop('page', '1')
        params['page'] = page

    except:
        return jsonify({"error": "An error has occurred while applying the filters"}), 500

    try:
        (sites, total) = list_historic_sites_with_filters(**params)
        json = [s.json() for s in sites]

        json_data = {
            "sites": json,
            "total": total,
            "per_page": per_page,
            "page": int(page),
        }

        return jsonify(json_data), 200
    except (ValueError, SQLAlchemyError) as e:
        return handle_db_error(
            e,
            "Error getting historic sites",
            "Ocurrió un error al obtener las sitios históricos. Por favor, intente nuevamente.",
            "historic_sites/index.html",
        )


