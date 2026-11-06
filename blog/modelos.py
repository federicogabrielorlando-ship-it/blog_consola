# Clases del blog: Autor, Post y Blog.
# Tambien estan las funciones que arman los objetos a partir de los
# diccionarios que vienen del JSON (el camino inverso de to_dict).
# Este archivo no importa nada del resto del paquete.

# Reglas fijas del sistema
estados_post = ("borrador", "publicado", "archivado")
claves_post = ("id", "titulo", "contenido", "autor", "tags", "estado")


class Autor:
    def __init__(self, nombre, bio, especialidad, redes_sociales):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = redes_sociales

    def to_dict(self):
        # Paso el autor a diccionario para poder guardarlo en JSON
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": self.redes_sociales
        }


class Post:
    def __init__(self, id, titulo, contenido, autor, tags, estado):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor  # es un objeto Autor, no un texto
        self.tags = tags
        self.estado = estado

    def tiene_tag(self, tag):
        # True si el post tiene ese tag (sin importar mayusculas)
        if not isinstance(self.tags, list):
            return False
        for etiqueta in self.tags:
            # Si algun tag no es texto lo salteo en vez de romper con .lower()
            if isinstance(etiqueta, str) and etiqueta.lower() == tag.lower():
                return True
        return False

    def resumen(self):
        # Una linea con titulo, autor y estado para mostrar en el listado
        titulo = self.titulo
        if not isinstance(titulo, str) or titulo.strip() == "":
            titulo = "(sin titulo)"
        return f"{titulo} | Autor: {self.autor.nombre} | Estado: {self.estado}"

    def to_dict(self):
        # Paso el post a diccionario. El autor tambien se convierte.
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.to_dict(),
            "tags": self.tags,
            "estado": self.estado
        }


class Blog:
    def __init__(self, posts):
        self.posts = posts  # lista de objetos Post
        self.hay_cambios = False  # para avisar si quedo algo sin guardar

    def listar_posts(self):
        return self.posts

    def buscar_por_titulo(self, termino):
        # Posts cuyo titulo contiene el termino, sin importar mayusculas
        resultados = []
        for post in self.posts:
            if isinstance(post.titulo, str) and termino.lower() in post.titulo.lower():
                resultados.append(post)
        return resultados

    def filtrar_por_tag(self, tag):
        resultados = []
        for post in self.posts:
            if post.tiene_tag(tag):
                resultados.append(post)
        return resultados

    def proximo_id(self):
        # El id mas alto que haya + 1 (si el blog esta vacio arranca en 1)
        mayor = 0
        for post in self.posts:
            if isinstance(post.id, int) and post.id > mayor:
                mayor = post.id
        return mayor + 1

    def crear_post(self, titulo, contenido, autor, tags, estado):
        # Creo el objeto Post y lo agrego a la lista del blog
        nuevo = Post(self.proximo_id(), titulo, contenido, autor, tags, estado)
        self.posts.append(nuevo)
        self.hay_cambios = True
        return nuevo

    def a_diccionarios(self):
        # La lista de posts convertida a diccionarios, lista para el JSON
        lista = []
        for post in self.posts:
            lista.append(post.to_dict())
        return lista


def crear_autor_desde_dict(datos):
    # Arma un Autor desde un diccionario. Devuelve (autor, mensaje)
    # o (None, mensaje) si el diccionario no sirve.
    if not isinstance(datos, dict):
        return None, "el autor no es un diccionario"
    if "nombre" not in datos:
        return None, 'al autor le falta la clave "nombre"'
    autor = Autor(
        datos["nombre"],
        datos.get("bio", ""),
        datos.get("especialidad", ""),
        datos.get("redes_sociales", [])
    )
    return autor, "ok"


def crear_post_desde_dict(datos):
    # Arma un Post desde un diccionario del JSON ("rehidratar" el objeto).
    # Si al diccionario le falta algo devuelvo (None, mensaje) en vez de romper.
    if not isinstance(datos, dict):
        return None, "el post no es un diccionario"

    for clave in claves_post:
        if clave not in datos:
            return None, f'falta la clave "{clave}"'

    autor, mensaje = crear_autor_desde_dict(datos["autor"])
    if autor is None:
        return None, mensaje

    post = Post(
        datos["id"],
        datos["titulo"],
        datos["contenido"],
        autor,
        datos["tags"],
        datos["estado"]
    )
    return post, "ok"
