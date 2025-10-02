from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.handlers.auth import role_required
from src.core.models.auth import RolUsuario
from src.core.models.auth import (
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    get_usuario_by_id,
    RolUsuario,
    buscar_usuarios,
    EmailExistente)

bp_user = Blueprint("user", __name__, url_prefix="/usuarios")

# Ruta raiz
@bp_user.route("/")
# @permission_required('user_index')
@role_required([RolUsuario.ADMIN])
def list_users(_session_user):
    email = request.args.get("email")
    activo = request.args.get("activo")
    rol = request.args.get("rol")
    orden = request.args.get("orden", "desc")
    pagina = int(request.args.get("pagina", 1))

    # Convertir activo a boolean si viene
    if activo == "SI":
        activo = True
    elif activo == "NO":
        activo = False
    else:
        activo = None

    usuarios, total = buscar_usuarios(
        email=email,
        activo=activo,
        rol=rol,
        orden=orden,
        pagina=pagina,
    )

    return render_template(
        "user_list.html",
        usuarios=usuarios,
        total=total,
        pagina=pagina,
        por_pagina=10
    )

# Crear usuario
@bp_user.route("/nuevo", methods=["GET", "POST"])
# @permission_required('user_new')
@role_required([RolUsuario.ADMIN])
def new_user():
    if request.method == "POST":
        email = request.form["email"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        rol = request.form["rol"]

        try:
            usuario, password_plano = crear_usuario(email, nombre, apellido, rol)
            # mostramos la contraseña generada al usuario
            flash(f"Usuario creado con éxito. La contraseña es: {password_plano}", "success")
            return redirect(url_for("user.list_users"))
        except EmailExistente:
            flash(f"El email {email} ya se encuentra registrado", "error")
            return render_template("user_form.html", action="Nuevo")

    return render_template("user_form.html", action="Nuevo")

# Actualizar usuario
@bp_user.route("/actualizar/<int:usuario_id>", methods=["GET", "POST"])
# @permission_required('user_update')
@role_required([RolUsuario.ADMIN])
def update_user(usuario_id):
    if request.method == "POST":
        usuario = actualizar_usuario(
            usuario_id,
            email=request.form["email"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            rol=request.form["rol"],
            activo="activo" in request.form
        )
        if not usuario:
            return "Usuario no encontrado", 404
        return redirect(url_for("user.list_users"))

    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return "Usuario no encontrado", 404
    return render_template("user_form.html", action="Actualizar", user=usuario, RolUsuario=RolUsuario)

# Eliminar usuario
@bp_user.route("/eliminar/<int:usuario_id>", methods=["GET", "POST"])
# @permission_required('user_destroy')
@role_required([RolUsuario.ADMIN])
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
