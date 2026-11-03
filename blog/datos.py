# Datos base del blog (vienen de las preentregas anteriores).
# Aca solo hay datos: nada de funciones ni de input().

perfil_autor = {
    "nombre": "Federico Orlando",
    "bio": "Economista. Trabajo con datos y estoy aprendiendo Python para analisis.",
    "especialidad": "Analisis de datos",
    "redes_sociales": ["linkedin.com/in/federico-orlando-4626242aa", "github.com/federicogabrielorlando-ship-it"]
}

estados_post = ("borrador", "publicado", "archivado")

etiquetas_blog = {"Python", "Datos", "Pandas", "Estadistica", "Economia", "Python"}

# Claves que tiene que tener cada post
claves_post = ("id", "titulo", "contenido", "autor", "tags", "estado")

posts = [
    {
        "id": 1,
        "titulo": "Mi primer script en Python",
        "contenido": "Como arme el entorno virtual y corri mi primer programa.",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Listas, tuplas, sets y diccionarios",
        "contenido": "Cuando conviene usar cada coleccion para guardar datos.",
        "autor": perfil_autor,
        "tags": ["Python", "Datos"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Como calcular la inflacion mensual con Python",
        "contenido": "Uso los datos del IPC para calcular la variacion de un mes a otro.",
        "autor": perfil_autor,
        "tags": ["Python", "Economia", "Estadistica"],
        "estado": "archivado"
    },
    # Posts con errores a proposito para probar la validacion
    {
        "id": 4,
        "titulo": "Primeros pasos con Pandas",
        "autor": perfil_autor,
        "tags": ["Pandas", "Datos"],
        "estado": "borrador"
    },
    {
        "id": 5,
        "titulo": "",
        "contenido": "Post que quedo sin titulo.",
        "autor": perfil_autor,
        "tags": ["Python"],
        "estado": "publicado"
    },
    {
        "id": 6,
        "titulo": "Graficos con matplotlib",
        "contenido": "Como hacer un grafico de lineas.",
        "autor": perfil_autor,
        "tags": "Python",
        "estado": "pendiente"
    }
]
