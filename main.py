# Preentrega 6 - Blog por consola con POO y JSON
# Federico Orlando
#
# Este archivo solo coordina: carga los posts desde posts.json, crea el objeto
# Blog y segun la opcion del menu llama a sus metodos. Se ejecuta con: python main.py

from blog.datos import ruta_posts, perfil_autor, cargar_posts, guardar_posts
from blog.modelos import Blog, crear_autor_desde_dict
from blog.menu import mostrar_menu, pedir_texto, pedir_datos_post, preguntar_si_no
from blog.operaciones import mostrar_posts, mostrar_conteo_por_estado
from blog.validaciones import validar_todos


def iniciar_blog():
    # Leo el JSON, muestro los avisos si hubo problemas y armo el Blog
    posts, avisos = cargar_posts(ruta_posts)
    for aviso in avisos:
        print("Aviso:", aviso)
    print(f"Se cargaron {len(posts)} posts desde {ruta_posts.name}")
    return Blog(posts)


def guardar_blog(blog):
    # Convierto los objetos a diccionarios y recien ahi los guardo
    ok, mensaje = guardar_posts(ruta_posts, blog.a_diccionarios())
    print(mensaje)
    if ok:
        blog.hay_cambios = False


def ejecutar_blog():
    blog = iniciar_blog()
    # El autor de los posts nuevos es el del perfil (tambien como objeto Autor)
    autor, mensaje = crear_autor_desde_dict(perfil_autor)

    # Bucle principal: muestra el menu hasta que el usuario elige salir
    while True:
        opcion = mostrar_menu()

        # Si no escribio un numero vuelvo a mostrar el menu
        if opcion is None:
            continue

        if opcion == 1:
            print("\nPosts disponibles:")
            mostrar_posts(blog.listar_posts())
            mostrar_conteo_por_estado(blog.listar_posts())

        elif opcion == 2:
            termino = pedir_texto("Buscar por titulo: ")
            if termino == "":
                print("La busqueda no puede estar vacia")
            else:
                encontrados = blog.buscar_por_titulo(termino)
                if len(encontrados) == 0:
                    print("No se encontraron posts con ese titulo")
                else:
                    print("\nResultados:")
                    mostrar_posts(encontrados)

        elif opcion == 3:
            tag = pedir_texto("Ingresa un tag: ")
            if tag == "":
                print("El tag no puede estar vacio")
            else:
                encontrados = blog.filtrar_por_tag(tag)
                if len(encontrados) == 0:
                    print("No hay posts con el tag", tag)
                else:
                    print("\nPosts con el tag", tag + ":")
                    mostrar_posts(encontrados)

        elif opcion == 4:
            titulo, contenido, tags, estado = pedir_datos_post()
            nuevo = blog.crear_post(titulo, contenido, autor, tags, estado)
            print(f"Post creado con id {nuevo.id}. Acordate de guardar (opcion 6).")

        elif opcion == 5:
            print("\nValidacion de posts:")
            validar_todos(blog.listar_posts())

        elif opcion == 6:
            guardar_blog(blog)

        elif opcion == 7:
            if blog.hay_cambios:
                if preguntar_si_no("Hay cambios sin guardar. ¿Guardar antes de salir? (s/n): "):
                    guardar_blog(blog)
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    ejecutar_blog()
