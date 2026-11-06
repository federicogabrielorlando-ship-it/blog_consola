# Datos base y persistencia del blog.
# Aca esta la ruta al archivo posts.json, el perfil del autor y las funciones
# que leen y guardan los posts. No hay menu ni input().

import json
from pathlib import Path

from blog.modelos import crear_post_desde_dict

# Armo la ruta desde la ubicacion de este archivo, asi funciona
# aunque el programa se ejecute desde otra carpeta
ruta_posts = Path(__file__).parent.parent / "posts.json"

# Autor que uso para los posts nuevos que se crean desde el menu
perfil_autor = {
    "nombre": "Federico Orlando",
    "bio": "Economista. Trabajo con datos y estoy aprendiendo Python para analisis.",
    "especialidad": "Analisis de datos",
    "redes_sociales": ["linkedin.com/in/federico-orlando-4626242aa", "github.com/federicogabrielorlando-ship-it"]
}


def cargar_posts(ruta):
    # Lee el JSON y devuelve (lista de objetos Post, lista de avisos).
    # Si el archivo no sirve devuelvo la lista vacia y el aviso, sin romper.
    avisos = []

    if not ruta.exists():
        avisos.append(f"No se encontro {ruta.name}. El blog arranca vacio y el archivo se crea al guardar.")
        return [], avisos

    with open(ruta, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    if texto.strip() == "":
        avisos.append(f"{ruta.name} esta vacio. El blog arranca sin posts.")
        return [], avisos

    try:
        datos = json.loads(texto)
    except json.JSONDecodeError:
        avisos.append(f"{ruta.name} no tiene un JSON valido. El blog arranca sin posts y el archivo no se toca hasta que guardes.")
        return [], avisos

    if not isinstance(datos, list):
        avisos.append(f"{ruta.name} tendria que tener una lista de posts. El blog arranca sin posts.")
        return [], avisos

    posts = []
    numero = 1
    for diccionario in datos:
        post, mensaje = crear_post_desde_dict(diccionario)
        if post is None:
            avisos.append(f"Se salteo el post {numero} del archivo: {mensaje}")
        else:
            posts.append(post)
        numero += 1

    return posts, avisos


def guardar_posts(ruta, lista):
    # Guarda una lista de diccionarios en el JSON. Devuelve (True/False, mensaje).
    if not isinstance(lista, list):
        return False, "No se guardo: lo que se quiere guardar no es una lista."

    # JSON no sabe guardar objetos: reviso que todo ya este pasado a diccionario
    for elemento in lista:
        if not isinstance(elemento, dict):
            return False, "No se guardo: hay un post que no se convirtio a diccionario (falta usar to_dict()). El archivo no se modifico."

    # Paso todo a texto antes de abrir el archivo, asi si algo falla no se pisa a medias
    texto = json.dumps(lista, indent=4, ensure_ascii=False)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

    return True, f"Se guardaron {len(lista)} posts en {ruta.name}"
