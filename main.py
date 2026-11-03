# Preentrega 5 - Blog por consola organizado en modulos y paquetes
# Federico Orlando
#
# Este archivo solo coordina: trae las piezas del paquete blog/ y las usa
# segun la opcion que elige el usuario. Se ejecuta con: python main.py

from blog.datos import posts
from blog.menu import mostrar_menu, pedir_texto
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_todos


def ejecutar_blog():
    # Bucle principal: muestra el menu hasta que el usuario elige salir
    while True:
        opcion = mostrar_menu()

        # Si no escribio un numero vuelvo a mostrar el menu
        if opcion is None:
            continue

        if opcion == 1:
            print("\nPosts disponibles:")
            listar_posts(posts)

        elif opcion == 2:
            termino = pedir_texto("Buscar por titulo: ")
            if termino == "":
                print("La busqueda no puede estar vacia")
            else:
                encontrados = buscar_por_titulo(posts, termino)
                if len(encontrados) == 0:
                    print("No se encontraron posts con ese titulo")
                else:
                    print("\nResultados:")
                    listar_posts(encontrados)

        elif opcion == 3:
            tag = pedir_texto("Ingresa un tag: ")
            if tag == "":
                print("El tag no puede estar vacio")
            else:
                encontrados = filtrar_por_tag(posts, tag)
                if len(encontrados) == 0:
                    print("No hay posts con el tag", tag)
                else:
                    print("\nPosts con el tag", tag + ":")
                    listar_posts(encontrados)

        elif opcion == 4:
            print("\nValidacion de posts:")
            validar_todos(posts)

        elif opcion == 5:
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    ejecutar_blog()
