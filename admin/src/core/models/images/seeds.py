import random
from uuid import uuid1
from flask import current_app
from datetime import datetime, timedelta, timezone
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.images.image import Image
import os
from os import abort, fstat
from uuid import uuid1

IMAGES_PER_SITE = 3

IMAGENES_DIR = "src/seed_data/"

IMAGENES = [
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg",
    "5.jpg",
    "6.jpg",
    "7.jpg",
    "8.jpg",
    "9.jpg",
    "10.jpg",
    "11.jpg",
    "12.jpg",
    "13.jpg",
    "14.jpg",
    "15.jpg",
    "16.jpg",
    "17.jpg",
    "18.jpg",
    "19.jpg",
    "20.jpg",
]


def seed_images():
    """Crea varias imagenes por sitio, usar con moderacion"""
    imagenes = []
    sitios = db.session.query(HistoricSites).all()

    client = current_app.storage
    bucket_name = current_app.config["MINIO_BUCKET"]

    for site in sitios:
        current = random.randint(0, len(IMAGENES) - 1)
        for j in range(IMAGES_PER_SITE):

            file_name = IMAGENES[current]
            file_path = f"{IMAGENES_DIR}{file_name}"
            with open(file_path, 'rb') as file:
                # Guardar en Minio
                _, ext = os.path.splitext(file_name)
                ext = ext.lower()
                size = fstat(file.fileno()).st_size
                object_name = f"public/{str(uuid1())}{ext}"
                content_type = f"image/{ext.lstrip('.')}" if ext else "application/octet-stream"
                client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=file,
                    length=size,
                    content_type=content_type,
                )

                # Guardar en la bd
                imagen = Image(
                    nombre=object_name,
                    titulo=f"Titulo de la imagen numero {j + 1}.",
                    desc=f"Esta es la descripcion de la imagen numero {j + 1}.",
                    orden=j,
                    sitio=site.id
                )
                imagenes.append(imagen)

                current += 1
                if current == len(IMAGENES):
                    current = 0

    db.session.add_all(imagenes)
    db.session.commit()
    print(f"Seed completo: {len(sitios) * IMAGES_PER_SITE} imagenes creadas.")
