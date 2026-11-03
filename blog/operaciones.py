# Funciones principales del blog: listar, buscar y filtrar.
# Todas reciben la lista de posts por parametro, no usan variables globales.


def obtener_nombre_autor(post):
    # Devuelve el nombre del autor sin romper si falta algun dato
    autor = post.get("autor")
    if isinstance(autor, dict):
        return autor.get("nombre", "Sin autor")
    return "Sin autor"


def listar_posts(lista):
    # Recorre la lista y muestra titulo, autor y estado de cada post
    if len(lista) == 0:
        print("No hay posts para mostrar")
        return
    for post in lista:
        titulo = post.get("titulo") or "(sin titulo)"
        estado = post.get("estado", "sin estado")
        print("-", titulo, "| Autor:", obtener_nombre_autor(post), "| Estado:", estado)


def buscar_por_titulo(lista, termino):
    # Devuelve una lista con los posts cuyo titulo contiene el termino
    resultados = []
    for post in lista:
        titulo = post.get("titulo", "")
        if isinstance(titulo, str) and termino.lower() in titulo.lower():
            resultados.append(post)
    return resultados


def filtrar_por_tag(lista, tag):
    # Devuelve una lista con los posts que tienen ese tag
    resultados = []
    for post in lista:
        tags = post.get("tags", [])
        if not isinstance(tags, list):
            continue  # si tags no es una lista salteo el post
        for etiqueta in tags:
            if etiqueta.lower() == tag.lower():
                resultados.append(post)
                break
    return resultados
