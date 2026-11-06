# Pruebas del blog: un caso por cada regla de validacion, la carga y el
# guardado del JSON con archivos buenos y rotos, y buscar/filtrar.
# Se ejecuta con: python pruebas.py

import json
from pathlib import Path

from blog.datos import cargar_posts, guardar_posts, perfil_autor
from blog.modelos import Autor, Post, Blog, crear_autor_desde_dict, crear_post_desde_dict
from blog.operaciones import contar_por_estado
from blog.validaciones import validar_post

resultados = {"ok": 0, "falla": 0}


def probar(descripcion, obtenido, esperado):
    # Compara lo que devolvio el programa con lo que esperaba
    if obtenido == esperado:
        resultados["ok"] += 1
        print("OK   ", descripcion)
    else:
        resultados["falla"] += 1
        print("FALLA", descripcion, "| esperaba:", esperado, "| obtuve:", obtenido)


def post_de_prueba():
    # Un post correcto que despues rompo de a una regla por vez
    autor = Autor("Federico Orlando", "Economista", "Analisis de datos", [])
    return Post(1, "Titulo", "Contenido", autor, ["Python"], "borrador")


# --- validar_post: un caso por regla ---
print("\nValidaciones")
probar("post correcto", validar_post(post_de_prueba()), (True, "válido"))
probar("no es un Post", validar_post({"titulo": "x"}), (False, "no es un objeto Post"))

p = post_de_prueba()
p.titulo = "   "
probar("titulo vacio", validar_post(p), (False, "el titulo esta vacio"))

p = post_de_prueba()
p.titulo = 123
probar("titulo que no es texto", validar_post(p), (False, "el titulo esta vacio"))

p = post_de_prueba()
p.contenido = ""
probar("contenido vacio", validar_post(p), (False, "el contenido esta vacio"))

p = post_de_prueba()
p.autor = "Federico"
probar("autor como texto", validar_post(p), (False, "el autor no es un objeto Autor"))

p = post_de_prueba()
p.autor.nombre = ""
probar("autor con nombre vacio", validar_post(p), (False, "el autor no tiene nombre"))

p = post_de_prueba()
p.autor.nombre = None
probar("autor con nombre None", validar_post(p), (False, "el autor no tiene nombre"))

p = post_de_prueba()
p.tags = "Python"
probar("tags como texto", validar_post(p), (False, "tags no es una lista"))

p = post_de_prueba()
p.tags = ["Python", 5]
probar("un tag que no es texto", validar_post(p), (False, "el tag 5 no es un texto"))

p = post_de_prueba()
p.estado = "pendiente"
probar("estado invalido", validar_post(p), (False, 'el estado "pendiente" no es valido'))

# --- Reconstruir objetos desde diccionarios ---
print("\nDiccionario -> objeto")
diccionario = post_de_prueba().to_dict()
post, mensaje = crear_post_desde_dict(diccionario)
probar("diccionario completo arma un Post", isinstance(post, Post), True)
probar("el autor queda como objeto Autor", isinstance(post.autor, Autor), True)

incompleto = post_de_prueba().to_dict()
del incompleto["contenido"]
probar("diccionario sin contenido", crear_post_desde_dict(incompleto), (None, 'falta la clave "contenido"'))

sin_nombre = post_de_prueba().to_dict()
del sin_nombre["autor"]["nombre"]
probar("autor sin nombre", crear_post_desde_dict(sin_nombre), (None, 'al autor le falta la clave "nombre"'))

probar("autor que no es diccionario", crear_autor_desde_dict("Federico"), (None, "el autor no es un diccionario"))
probar("post que no es diccionario", crear_post_desde_dict([1, 2]), (None, "el post no es un diccionario"))

# --- Carga y guardado del JSON en una carpeta aparte ---
print("\nArchivo JSON")
carpeta = Path(__file__).parent / "pruebas_tmp"
carpeta.mkdir(exist_ok=True)
archivo = carpeta / "posts.json"
if archivo.exists():
    archivo.unlink()

posts, avisos = cargar_posts(archivo)
probar("archivo que no existe: blog vacio y aviso", (len(posts), len(avisos)), (0, 1))

archivo.write_text("", encoding="utf-8")
posts, avisos = cargar_posts(archivo)
probar("archivo vacio: blog vacio y aviso", (len(posts), len(avisos)), (0, 1))

archivo.write_text('[{"id": 1, "titulo": "roto",]', encoding="utf-8")
posts, avisos = cargar_posts(archivo)
probar("JSON mal escrito: blog vacio y aviso", (len(posts), len(avisos)), (0, 1))

archivo.write_text('{"id": 1}', encoding="utf-8")
posts, avisos = cargar_posts(archivo)
probar("JSON que no es lista: blog vacio y aviso", (len(posts), len(avisos)), (0, 1))

archivo.write_text(json.dumps([incompleto]), encoding="utf-8")
posts, avisos = cargar_posts(archivo)
probar("post incompleto en el archivo: se saltea", (len(posts), avisos), (0, ['Se salteo el post 1 del archivo: falta la clave "contenido"']))

texto_antes = archivo.read_text(encoding="utf-8")
blog = Blog([post_de_prueba()])
ok, mensaje = guardar_posts(archivo, blog.posts)
probar("guardar objetos sin to_dict no se permite", ok, False)
probar("y el archivo anterior no se toco", archivo.read_text(encoding="utf-8"), texto_antes)

autor, mensaje = crear_autor_desde_dict(perfil_autor)
blog.crear_post("Mi post nuevo con tildes: análisis", "Probando el guardado", autor, ["JSON"], "publicado")
ok, mensaje = guardar_posts(archivo, blog.a_diccionarios())
probar("guardar despues de to_dict", ok, True)

# Simulo cerrar y volver a abrir el programa: cargo de nuevo el archivo
posts, avisos = cargar_posts(archivo)
probar("al volver a cargar estan los 2 posts", len(posts), 2)
probar("el post nuevo sigue con su titulo (y las tildes)", posts[1].titulo, "Mi post nuevo con tildes: análisis")
probar("el post nuevo tomo el id 2", posts[1].id, 2)

archivo.unlink()
carpeta.rmdir()

# --- Buscar, filtrar y contar ---
print("\nBuscar, filtrar y contar")
p_raro = post_de_prueba()
p_raro.id = 2
p_raro.titulo = ""
p_raro.tags = ["Datos", 7]
p_texto = post_de_prueba()
p_texto.id = 3
p_texto.tags = "Python"
p_texto.estado = "publicado"
blog = Blog([post_de_prueba(), p_raro, p_texto])

probar("buscar ignora mayusculas", len(blog.buscar_por_titulo("TITULO")), 2)
probar("buscar algo que no existe", blog.buscar_por_titulo("django"), [])
probar("filtrar ignora mayusculas", len(blog.filtrar_por_tag("pYtHoN")), 1)
probar("filtrar con un tag que no es texto no rompe", len(blog.filtrar_por_tag("datos")), 1)
probar("contar por estado", contar_por_estado(blog.posts), {"borrador": 2, "publicado": 1})

print(f"\nResultado: {resultados['ok']} OK, {resultados['falla']} con falla")
