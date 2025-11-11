from src.core.database import db
from src.core.models.images.image import Image
from sqlalchemy.exc import IntegrityError
from flask import current_app
from sqlalchemy import select

class ErrorAlGuardar(Exception):
    """Ocurrio un error al guardar las imagenes."""
    pass

def get_bucket_url():
    server = current_app.config["MINIO_SERVER"]
    secure = current_app.config["MINIO_SECURE"]
    bucket = current_app.config["MINIO_BUCKET"]
    if secure:
        secure = "s"
    else:
        secure = ""
    return f"http{secure}://{server}/{bucket}"


def guardar_imagenes(nombres, titulos, descripciones, sitio):
    for i in range(len(nombres)):
        imagen = Image(
            nombre=nombres[i],
            titulo=titulos[i],
            desc=descripciones[i],
            orden=i,
            sitio=sitio,
        )
        db.session.add(imagen)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ErrorAlGuardar

def get_images_by_site(id):
    bucket_url = get_bucket_url()
    images = db.session.query(Image).filter_by(sitio=id).order_by(Image.orden).all()
    for image in images:
        image.url = f"{bucket_url}/{image.nombre}"
    return images

def get_images_map(site_id: int):
    """Retorna las imagenes en un diccionario, usando el nombre como clave."""
    imgs = db.session.execute(
        select(Image).where(Image.sitio == site_id)
    ).scalars().all()
    return {img.nombre: img for img in imgs}, imgs

def guardar_imagen(nombre, titulo, desc, orden, sitio):
    """Guarda una imagen en la BD. No hace Commit()"""
    img = Image(
        nombre=nombre,
        titulo=titulo,
        desc=desc,
        orden=orden,
        sitio=sitio,
    )
    db.session.add(img)
    return img

def delete_image(img: Image):
    """Elimina la imagen de la BD. No hace Commit()"""
    db.session.delete(img)

def save_changes():
    """Intenta hacer commit(), si falla hace rollback()"""
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise ErrorAlGuardar
