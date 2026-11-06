# Funciones para mostrar los posts en pantalla y hacer cuentas sobre ellos.
# Como en la entrega anterior, todas reciben la lista de posts por parametro.
# Buscar y filtrar ahora son metodos de la clase Blog (blog/modelos.py).


def mostrar_posts(lista):
    # Muestra titulo, autor y estado de cada post
    if len(lista) == 0:
        print("No hay posts para mostrar")
        return
    for post in lista:
        print("-", post.resumen())


def contar_por_estado(lista):
    # Devuelve un diccionario {estado: cantidad de posts}
    conteo = {}
    for post in lista:
        estado = post.estado
        if estado in conteo:
            conteo[estado] += 1
        else:
            conteo[estado] = 1
    return conteo


def mostrar_conteo_por_estado(lista):
    conteo = contar_por_estado(lista)
    if len(conteo) == 0:
        return
    print("\nCantidad de posts por estado:")
    for estado in conteo:
        print(f"- {estado}: {conteo[estado]}")
