from src.core.database import db
from src.core.models.images.image import Image
from sqlalchemy.exc import IntegrityError
from flask import current_app

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
