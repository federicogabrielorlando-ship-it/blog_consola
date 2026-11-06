# Reglas para saber si un post esta bien armado.
# Ahora los posts son objetos Post, asi que reviso sus atributos.
# Importo de modelos.py las clases y las reglas fijas. modelos.py no importa nada,
# asi no hay imports circulares.

from blog.modelos import Autor, Post, estados_post


def validar_post(post):
    # Revisa un post y devuelve (True, "válido") o (False, "mensaje con el error")
    if not isinstance(post, Post):
        return False, "no es un objeto Post"

    if not isinstance(post.titulo, str) or post.titulo.strip() == "":
        return False, "el titulo esta vacio"

    if not isinstance(post.contenido, str) or post.contenido.strip() == "":
        return False, "el contenido esta vacio"

    if not isinstance(post.autor, Autor):
        return False, "el autor no es un objeto Autor"

    # No alcanza con que exista el nombre: tiene que ser un texto con algo escrito
    if not isinstance(post.autor.nombre, str) or post.autor.nombre.strip() == "":
        return False, "el autor no tiene nombre"

    if not isinstance(post.tags, list):
        return False, "tags no es una lista"

    # Cada tag tiene que ser texto (si no, despues falla el .lower() del filtro)
    for etiqueta in post.tags:
        if not isinstance(etiqueta, str):
            return False, f"el tag {etiqueta} no es un texto"

    if post.estado not in estados_post:
        return False, f'el estado "{post.estado}" no es valido'

    return True, "válido"


def validar_todos(lista):
    # Usa validar_post en cada post y muestra el resultado
    if len(lista) == 0:
        print("No hay posts para validar")
        return
    for post in lista:
        es_valido, mensaje = validar_post(post)
        if es_valido:
            print(f"Post {post.id}: válido")
        else:
            print(f"Post {post.id}: error - {mensaje}")
