from flask import Blueprint, render_template, request, redirect, url_for
from src.core.models.auth import (get_all_usuarios,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    get_usuario_by_id,
    RolUsuario)

bp_user = Blueprint("user", __name__, url_prefix="/usuarios")

# Ruta raiz
@bp_user.route("/")
def list_users():
    usuarios = get_all_usuarios()
    return render_template("user_list.html", users=usuarios)

# Crear usuario
@bp_user.route("/nuevo", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        crear_usuario(
            email=request.form["email"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            password="temp",
            rol=RolUsuario(request.form["rol"])
        )
        return redirect(url_for("user.list_users"))
    return render_template("user_form.html", action="Nuevo")

# Actualizar usuario
@bp_user.route("/actualizar/<int:usuario_id>", methods=["GET", "POST"])
def update_user(usuario_id):
    if request.method == "POST":
        usuario = actualizar_usuario(
            usuario_id,
            rol=RolUsuario(request.form["rol"]),
            activo="activo" in request.form
        )
        if not usuario:
            return "Usuario no encontrado", 404
        return redirect(url_for("user.list_users"))

    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return "Usuario no encontrado", 404
    return render_template("user_form.html", action="Actualizar", user=usuario)

# Eliminar usuario
@bp_user.route("/eliminar/<int:usuario_id>", methods=["GET", "POST"])
def delete_user(usuario_id):
    if request.method == "POST":
        usuario = eliminar_usuario(usuario_id)
        if not usuario:
            return "Usuario no encontrado", 404
        return redirect(url_for("user.list_users"))

    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return "Usuario no encontrado", 404
    return render_template("user_confirm_delete.html", user=usuario)
