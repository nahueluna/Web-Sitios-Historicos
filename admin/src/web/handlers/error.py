from dataclasses import dataclass
from flask import render_template

@dataclass
class HTTPError:
    code: int
    message: str
    description: str

def not_found(e):
    error = HTTPError (
        code = 404,
        message = "Página no encontrada",
        description = "Lo sentimos, la página que estás buscando no existe."
    )
    return render_template('error.html', error = error), 404

def unauthorized(e):
    error = HTTPError (
        code = 401,
        message = "Usuario no autenticado",
        description = "Asegúrese de autenticarse para acceder a la página."
    )
    return render_template('error.html', error = error), 401

def internal_server_error(e):
    error = HTTPError (
        code = 500,
        message = "Error interno en el servidor",
        description = "Lo sentimos, se ha producido un error en el servidor."
    )
    return render_template('error.html', error = error), 500

def method_not_allowed(e):
    error = HTTPError (
        code = 405,
        message = "Método no permitido",
        description = "Lo sentimos, la operación que intentas realizar no está permitida."
    )
    return render_template('error.html', error = error), 405