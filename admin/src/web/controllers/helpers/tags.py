import unicodedata
import re
from flask import Response

def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    )

def verify_tag_and_generate_slug(tag_name):
    if not tag_name:
        return Response("El ingreso de un nombre para el tag es obligatorio.", status=400)
    if not (3 <= len(tag_name) <= 50):
        return Response("El nombre de la etiqueta debe tener entre 3 y 50 caracteres.", status=400)

    slug_without_accents = remove_accents(tag_name).lower().replace(' ', '-')
    slug_without_special_chars = re.sub(r'[^a-zA-Z0-9\s-]', '', slug_without_accents)

    return slug_without_special_chars