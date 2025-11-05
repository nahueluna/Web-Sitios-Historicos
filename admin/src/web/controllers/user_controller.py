from flask import Blueprint, render_template, request, redirect, url_for, flash
# Modelos
from src.core.models.auth import RolUsuario
# Servicios de usuario
from src.core.models.auth import (crear_usuario, actualizar_usuario, eliminar_usuario, get_usuario_by_id, RolUsuario, buscar_usuarios, EmailExistente)
# Decoradores de permisos y autenticación
from src.web.handlers.auth import login_required, role_required
# Decoradores para feature flags y mantenimiento ()
from src.web.decorator import block_admin_maintenance

bp_user = Blueprint("user", __name__, url_prefix="/usuarios")

# Ruta raiz
@bp_user.route("/")
# @permission_required('user_index')
@role_required([RolUsuario.ADMIN])
@block_admin_maintenance
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

# Limpiar filtros aplicados al listado
@bp_user.route("/limpiar_filtros")
def clear_filters():
    return redirect(url_for("user.list_users"))

# Crear usuario
@bp_user.route("/nuevo", methods=["GET", "POST"])
# @permission_required('user_new')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def new_user(_session_user):
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
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def update_user(_session_user, usuario_id):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("user.list_users"))
    
    # Verificar si es system admin
    if usuario.system_admin:
        flash("No se puede modificar un usuario System Admin", "error")
        return redirect(url_for("user.list_users"))
    
    if request.method == "POST":
        try:
            usuario = actualizar_usuario(
                usuario_id,
                email=request.form["email"],
                nombre=request.form["nombre"],
                apellido=request.form["apellido"],
                rol=request.form["rol"],
                activo="activo" in request.form
            )
            if not usuario:
                flash("Usuario no encontrado", "error")
                return redirect(url_for("user.list_users"))
            
            flash("Usuario actualizado exitosamente", "success")
            return redirect(url_for("user.list_users"))
        except ValueError as e:
            # Capturar el error de intentar bloquear un administrador
            flash(str(e), "error")
            return render_template("user_form.html", action="Actualizar", user=usuario, RolUsuario=RolUsuario)
    
    return render_template("user_form.html", action="Actualizar", user=usuario, RolUsuario=RolUsuario)

# Eliminar usuario
@bp_user.route("/eliminar/<int:usuario_id>", methods=["GET", "POST"])
# @permission_required('user_destroy')
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def delete_user(_session_user, usuario_id):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("user.list_users"))
    
    # Verificar si es system admin antes de mostrar el formulario
    if usuario.system_admin:
        flash("No se puede eliminar un usuario System Admin", "error")
        return redirect(url_for("user.list_users"))
    
    if request.method == "POST":
        try:
            eliminar_usuario(usuario_id)
            flash(f"Usuario {usuario.email} eliminado exitosamente", "success")
            return redirect(url_for("user.list_users"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("user.list_users"))
    
    return render_template("user_confirm_delete.html", user=usuario)
