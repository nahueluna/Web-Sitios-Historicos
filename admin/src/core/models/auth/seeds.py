# src/core/database/seed.py
from src.core.database import db
from src.core.models.auth import Usuario, RolUsuario, hash_password
from datetime import datetime, timedelta


# También existe seeds_user.py, que crea roles, permisos y asigna permisos a roles
# Cantidad de usuarios a crear
CANTIDAD_USUARIOS = 60

def seed_usuarios():
    usuarios = []
    roles = [RolUsuario.PUBLICO, RolUsuario.EDITOR, RolUsuario.ADMIN]
    hora_actual = datetime.now()

    for i in range(1, CANTIDAD_USUARIOS + 1):
        usuario = Usuario(
            email=f"user{i}@example.com",
            nombre=f"Nombre{i}",
            apellido=f"Apellido{i}",
            password=hash_password("password"),
            activo=bool(i % 10),
            rol=roles[i % len(roles)],
            fecha_creacion=hora_actual - timedelta(seconds=i),
        )
        usuarios.append(usuario)

    db.session.add_all(usuarios)
    db.session.commit()
    print(f"Seed completo: {CANTIDAD_USUARIOS} usuarios creados.")
