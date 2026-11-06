# Todo lo que tiene que ver con hablar con el usuario: el menu y los input().

from blog.modelos import estados_post


def mostrar_menu():
    # Muestra el menu y devuelve la opcion como numero (o None si no es un numero)
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")
    try:
        opcion = int(input("Elegi una opcion: "))
        return opcion
    except ValueError:
        print("Error: tenes que escribir un numero del 1 al 7")
        return None


def pedir_texto(mensaje):
    # Pide un texto al usuario y lo devuelve sin espacios al principio ni al final
    texto = input(mensaje).strip()
    return texto


def pedir_texto_obligatorio(mensaje, campo):
    # Vuelve a preguntar mientras el usuario deje el campo vacio
    while True:
        texto = pedir_texto(mensaje)
        if texto != "":
            return texto
        print(f"El {campo} no puede quedar vacio, escribilo de nuevo.")


def pedir_tags():
    # Los tags se escriben separados por coma: "Python, Datos"
    while True:
        texto = pedir_texto_obligatorio("Tags (separados por coma): ", "campo de tags")
        tags = []
        for parte in texto.split(","):
            if parte.strip() != "":
                tags.append(parte.strip())
        if len(tags) > 0:
            return tags
        print("Tenes que escribir al menos un tag.")


def pedir_estado():
    # Si aprieta Enter queda como borrador
    while True:
        estado = pedir_texto("Estado (borrador, publicado o archivado) [Enter = borrador]: ").lower()
        if estado == "":
            return "borrador"
        if estado in estados_post:
            return estado
        print(f'"{estado}" no es un estado valido.')


def pedir_datos_post():
    # Pide todo lo necesario para un post nuevo y lo devuelve en una tupla
    print("\nNuevo post (el autor es el del perfil del blog)")
    titulo = pedir_texto_obligatorio("Titulo: ", "titulo")
    contenido = pedir_texto_obligatorio("Contenido: ", "contenido")
    tags = pedir_tags()
    estado = pedir_estado()
    return titulo, contenido, tags, estado


def preguntar_si_no(mensaje):
    # Devuelve True si responde s y False si responde n
    while True:
        respuesta = pedir_texto(mensaje).lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("Responde s o n.")
