# Blog por consola

Preentrega 6 del curso Fundamentos de programación con Python para datos (Coderhouse).
Autor: Federico Orlando.

## Qué hace

Es un blog que funciona en la terminal. Los posts se guardan en el archivo `posts.json`, así que lo que se crea en una ejecución sigue estando la próxima vez que se abre el programa. Desde un menú se puede:

1. Ver todos los posts (título, autor y estado, y al final cuántos hay de cada estado)
2. Buscar posts por título (no importan mayúsculas o minúsculas)
3. Filtrar posts por tag (no importan mayúsculas o minúsculas)
4. Crear un nuevo post
5. Validar posts (muestra cuáles están bien armados y cuál es el error de los que no)
6. Guardar los posts en `posts.json`
7. Salir (si hay cambios sin guardar, pregunta si se quieren guardar)

En `posts.json` hay 6 posts. Tres tienen errores a propósito (contenido vacío, título vacío, y tags como texto con un estado que no existe) para que se vea cómo funciona la validación.

## Cómo ejecutarlo

Necesita Python 3. No usa librerías externas (`json` y `pathlib` vienen con Python).

1. Abrir la terminal en la carpeta `blog_consola` (donde está `main.py`).
2. (Opcional) Activar el entorno virtual si se tiene uno: `.venv\Scripts\activate` en Windows o `source .venv/bin/activate` en Mac/Linux.
3. Ejecutar:

```
python main.py
```

4. Elegir una opción escribiendo un número del 1 al 7.

Para correr las pruebas:

```
python pruebas.py
```

## Cómo está organizado

```
blog_consola/
│
├── main.py
├── pruebas.py
├── posts.json
├── README.md
├── .gitignore
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── modelos.py
    ├── operaciones.py
    └── validaciones.py
```

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada. Carga los posts, crea el objeto `Blog` y según la opción del menú llama a sus métodos. El arranque está dentro de `if __name__ == "__main__":`. |
| `blog/__init__.py` | Hace que Python reconozca la carpeta `blog/` como un paquete. |
| `blog/modelos.py` | Las clases `Autor`, `Post` y `Blog`, las reglas fijas (`estados_post`, `claves_post`) y las funciones que arman objetos a partir de diccionarios. |
| `blog/datos.py` | Persistencia: la ruta a `posts.json`, el perfil del autor y las funciones `cargar_posts()` y `guardar_posts()`. |
| `blog/menu.py` | Todo lo que habla con el usuario: el menú y los `input()`, incluidos los datos de un post nuevo. |
| `blog/operaciones.py` | Mostrar los posts en pantalla y contarlos por estado (`contar_por_estado`). Reciben la lista por parámetro. |
| `blog/validaciones.py` | `validar_post()` revisa un objeto `Post` regla por regla y `validar_todos()` muestra el resultado de cada uno. |
| `pruebas.py` | 33 casos de prueba: cada regla de validación, archivos rotos, guardar y volver a cargar, buscar y filtrar. |
| `posts.json` | Los posts guardados. |
| `.gitignore` | Evita subir `__pycache__` y el entorno virtual. |

## Clases

**`Autor`**: la persona que escribe. Atributos: `nombre`, `bio`, `especialidad` y `redes_sociales`. Método `to_dict()` para pasarlo a diccionario.

**`Post`**: una publicación. Atributos: `id`, `titulo`, `contenido`, `autor`, `tags` y `estado`. El atributo `autor` es un objeto `Autor`, no un texto: un post *tiene* un autor (composición). Por eso el nombre se lee con `post.autor.nombre`. Métodos:
- `tiene_tag(tag)`: dice si el post tiene ese tag sin importar mayúsculas. Si `tags` no es una lista o algún tag no es texto, no rompe.
- `resumen()`: la línea que se muestra en el listado.
- `to_dict()`: pasa el post a diccionario, incluido el autor (llama a `autor.to_dict()`).

**`Blog`**: centraliza el manejo de los posts. Tiene el atributo `posts` (una lista de objetos `Post`) y `hay_cambios` (para avisar si quedó algo sin guardar). Métodos:
- `listar_posts()`: devuelve todos los posts.
- `buscar_por_titulo(termino)` y `filtrar_por_tag(tag)`: devuelven los posts que coinciden.
- `crear_post(titulo, contenido, autor, tags, estado)`: crea el objeto `Post` con el id siguiente y lo agrega a la lista.
- `proximo_id()`: el id más alto + 1.
- `a_diccionarios()`: la lista de posts convertida a diccionarios, lista para guardar.

## Cómo se guarda y se carga la información

JSON no sabe guardar objetos de Python, solo listas, diccionarios, textos, números y booleanos. Por eso el recorrido es:

```
Guardar:  objetos Post  ->  to_dict()  ->  lista de diccionarios  ->  posts.json
Cargar:   posts.json  ->  lista de diccionarios  ->  crear_post_desde_dict()  ->  objetos Post
```

1. Al iniciar, `main.py` llama a `cargar_posts(ruta_posts)`. Esa función lee el archivo, lo convierte con `json.loads()` y pasa cada diccionario por `crear_post_desde_dict()`, que arma el `Autor` y el `Post`. Con esa lista de objetos se crea el `Blog`.
2. Mientras el programa corre, todo se hace con objetos: el menú llama a los métodos del `Blog`.
3. Al guardar (opción 6, o al salir si se elige guardar), `blog.a_diccionarios()` convierte cada post con `to_dict()` y `guardar_posts()` escribe la lista en `posts.json` con `json.dumps()` (con `indent=4` y `ensure_ascii=False` para que se lea bien y respete las tildes).

La ruta a `posts.json` se arma con `Path(__file__)`, así el archivo se encuentra aunque el programa se ejecute desde otra carpeta.

## Manejo de errores

| Situación | Qué hace el programa |
|---|---|
| `posts.json` no existe | Avisa y arranca con el blog vacío. Al guardar se crea el archivo. |
| `posts.json` está vacío | Avisa y arranca con el blog vacío. |
| `posts.json` tiene un JSON mal escrito | Avisa que el JSON no es válido y arranca con el blog vacío. |
| El JSON no es una lista | Avisa y arranca con el blog vacío. |
| Un post del archivo está incompleto (le falta una clave o el autor no tiene nombre) | Avisa qué falta, saltea ese post y carga el resto. |
| Se intenta guardar un objeto sin convertirlo a diccionario | `guardar_posts()` lo detecta antes de escribir, avisa y no toca el archivo. |
| Se escribe texto en el menú | Avisa que hay que escribir un número del 1 al 7. |
| Se elige un número fuera del menú | Muestra "Opción inválida, intenta de nuevo". |
| Se deja un campo vacío al crear un post | Avisa y vuelve a pedir ese dato. Lo mismo si el estado no es borrador, publicado o archivado. |
| Búsqueda o tag vacíos | Avisa y vuelve al menú. |

## Qué cambió respecto a la Preentrega 5

- Se agregó `blog/modelos.py` con las clases `Autor`, `Post` y `Blog`. Los posts dejaron de ser diccionarios dentro del programa.
- Los posts ya no están escritos en `datos.py`: están en `posts.json`. `datos.py` ahora se encarga de cargarlos y guardarlos.
- Listar, buscar y filtrar pasaron a ser métodos de `Blog`. `operaciones.py` quedó para mostrar los posts y contarlos por estado.
- `validaciones.py` ahora revisa objetos `Post`.
- El menú pasó de 5 a 7 opciones: se agregaron crear post y guardar en JSON.

## Devoluciones aplicadas

**Preentrega 4**
- El nombre del autor tiene que ser un texto con algo escrito, no alcanza con que exista (`validar_post`: "el autor no tiene nombre").
- Antes de usar `.lower()` se revisa que cada tag sea texto (`Post.tiene_tag` saltea los que no lo son y `validar_post` avisa "el tag X no es un texto").
- Se probaron entradas no numéricas, opciones fuera de rango, búsquedas con distintas mayúsculas y posts incompletos (ver "Pruebas realizadas").
- `pruebas.py` tiene un caso por cada regla de `validar_post` y compara el mensaje exacto que devuelve.

**Preentrega 5**
- Se sumó `.gitignore` para no subir `__pycache__` ni el entorno virtual.
- Nueva operación en `operaciones.py` con el mismo patrón (recibe la lista por parámetro): `contar_por_estado(lista)`, que se muestra al final de la opción 1.
- El flujo de datos con persistencia es el de la sección "Cómo se guarda y se carga la información": `main.py` carga, el `Blog` trabaja con objetos y `datos.py` guarda. El menú no toca el archivo.

## Pruebas realizadas

- `python pruebas.py`: 33 casos OK.
- A mano con `python main.py`: listar, buscar con mayúsculas (`PYTHON`), buscar algo que no existe, búsqueda vacía, filtrar (`datos`, `Python`), escribir texto y números fuera de rango en el menú, crear un post dejando campos vacíos y con un estado inválido, validar, guardar y salir.
- Persistencia: crear un post, guardar, cerrar, volver a abrir y comprobar que el post sigue estando (por búsqueda y por tag).
- Archivo: ejecutar sin `posts.json`, con el archivo vacío, con un JSON mal escrito y con posts incompletos.
