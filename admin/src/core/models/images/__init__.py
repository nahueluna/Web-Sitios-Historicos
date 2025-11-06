from src.core.database import db
from src.core.models.images.image import Image
from sqlalchemy.exc import IntegrityError

class ErrorAlGuardar(Exception):
    """Ocurrio un error al guardar las imagenes."""
    pass

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
