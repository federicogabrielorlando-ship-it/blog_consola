# Reglas para saber si un post esta bien armado.
# Importo de datos.py solo las reglas fijas (claves y estados). datos.py no importa nada,
# asi no hay imports circulares.

from blog.datos import claves_post, estados_post


def validar_post(post):
    # Revisa un post y devuelve (True, "válido") o (False, "mensaje con el error")
    if not isinstance(post, dict):
        return False, "el post no es un diccionario"

    for clave in claves_post:
        if clave not in post:
            return False, f'falta la clave "{clave}"'

    if not isinstance(post["titulo"], str) or post["titulo"].strip() == "":
        return False, "el titulo esta vacio"

    if not isinstance(post["contenido"], str) or post["contenido"].strip() == "":
        return False, "el contenido esta vacio"

    if not isinstance(post["autor"], dict):
        return False, "el autor no es un diccionario"

    if "nombre" not in post["autor"]:
        return False, 'el autor no tiene la clave "nombre"'

    if not isinstance(post["tags"], list):
        return False, "tags no es una lista"

    if post["estado"] not in estados_post:
        return False, f'el estado "{post["estado"]}" no es valido'

    return True, "válido"


def validar_todos(lista):
    # Usa validar_post en cada post y muestra el resultado
    numero = 1
    for post in lista:
        es_valido, mensaje = validar_post(post)
        if es_valido:
            print(f"Post {numero}: válido")
        else:
            print(f"Post {numero}: error - {mensaje}")
        numero += 1
