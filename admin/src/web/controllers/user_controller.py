from flask import Blueprint, render_template, request, redirect, url_for

bp_user = Blueprint("user", __name__, url_prefix="/usuarios")

# Lista de usuarios hardcodeados
users = [
    {"id": 1, "email": "alice@example.com", "nombre": "Alice", "apellido": "Smith", "rol": "Usuario público"},
    {"id": 2, "email": "bob@example.com", "nombre": "Bob", "apellido": "Johnson", "rol": "Editor"},
]

# Funcion temporal de prueba
def print_users():
    print("=== Users ===")
    for u in users:
        print(u)

# Ruta raiz
@bp_user.route("/")
def list_users():
    return render_template("user_list.html", users=users)

# Crear usuario
@bp_user.route("/nuevo", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        new_id = max([u["id"] for u in users], default=0) + 1
        user = {
            "id": new_id,
            "email": request.form["email"],
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "rol": request.form["rol"],
        }
        users.append(user)
        print_users()
        return redirect(url_for("user.list_users"))
    return render_template("user_form.html", action="Nuevo")

# Actualizar usuario
@bp_user.route("/actualizar/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "Usuario no encontrado", 404

    if request.method == "POST":
        user["rol"] = request.form["rol"]
        print_users()
        return redirect(url_for("user.list_users"))

    return render_template("user_form.html", action="Actualizar", user=user)

# Eliminar usuario
@bp_user.route("/eliminar/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "Usuario no encontrado", 404

    if request.method == "POST":
        users.remove(user)
        print_users()
        return redirect(url_for("user.list_users"))

    return render_template("user_confirm_delete.html", user=user)
