from flask import Blueprint, request, flash, redirect, session, url_for
from flask import render_template
from src.core.models.auth import check_user

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.get("/")
def login():
    return render_template("auth/login.html")

@bp_auth.post("/authenticate")
def authenticate():
    email = request.form["email"]
    password = request.form["password"]
    user = check_user(email, password)
    if not user:
        flash("Credenciales Invalidas.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = email
    flash("Has iniciado sesión correctamente.", "success")
    return redirect("/")

@bp_auth.get("/logout")
def logout():
    if session.get("user"):
        session.pop("user")
        session.clear()
        flash("Has cerrado sesión correctamente.", "success")
    else:
        flash("No has iniciado sesión.", "error")
    return redirect(url_for("auth.login"))
