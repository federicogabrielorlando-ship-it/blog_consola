# Blog por consola

Preentrega 5 del curso Fundamentos de programación con Python para datos (Coderhouse).
Autor: Federico Orlando.

## Qué hace

Es un blog que funciona en la terminal. Los posts están guardados en memoria y desde un menú se puede:

1. Ver todos los posts (título, autor y estado)
2. Buscar posts por título (no importan mayúsculas o minúsculas)
3. Filtrar posts por tag (no importan mayúsculas o minúsculas)
4. Validar posts (muestra cuáles están bien armados y cuál es el error de los que no)
5. Salir

Algunos posts tienen errores a propósito (le falta el contenido, título vacío, tags como texto y un estado que no existe) para que se vea cómo funciona la validación.

## Cómo ejecutarlo

Necesita Python 3. No usa librerías externas.

1. Abrir la terminal en la carpeta `blog_consola` (donde está `main.py`).
2. (Opcional) Activar el entorno virtual si se tiene uno: `.venv\Scripts\activate` en Windows o `source .venv/bin/activate` en Mac/Linux.
3. Ejecutar:

```
python main.py
```

4. Elegir una opción escribiendo un número del 1 al 5.

Importante: hay que ejecutarlo desde la carpeta raíz del proyecto. Si se ejecuta desde otra carpeta, Python no encuentra el paquete `blog` y da error de importación.

## Cómo está organizado

```
blog_consola/
│
├── main.py
├── README.md
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── operaciones.py
    └── validaciones.py
```

## Qué hace cada archivo

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Archivo principal, el que se ejecuta. Importa las funciones del paquete `blog` y coordina el menú: según la opción elegida llama a la función que corresponde. El arranque está dentro de `if __name__ == "__main__":`. |
| `blog/__init__.py` | Hace que Python reconozca la carpeta `blog/` como un paquete. No tiene código, solo un comentario. |
| `blog/datos.py` | Datos base del blog: `perfil_autor`, `estados_post`, `etiquetas_blog`, `claves_post` y la lista `posts`. Cada post usa `perfil_autor` como autor (diccionario anidado). |
| `blog/menu.py` | Interacción con el usuario: `mostrar_menu()` muestra las opciones y devuelve la elegida (con `try/except` por si escribe texto) y `pedir_texto()` pide la búsqueda o el tag. |
| `blog/operaciones.py` | Funciones del blog: `listar_posts(lista)`, `buscar_por_titulo(lista, termino)` y `filtrar_por_tag(lista, tag)`. Reciben los datos por parámetro. |
| `blog/validaciones.py` | Reglas de validación: `validar_post(post)` revisa que el post sea un diccionario, que tenga todas las claves, que el título y el contenido no estén vacíos, que el autor sea un diccionario con nombre, que los tags sean una lista y que el estado sea válido. `validar_todos(lista)` muestra el resultado de cada post. |

## Cómo se conectan los archivos

`main.py` importa desde el paquete con la forma `from blog.modulo import funcion`:

```python
from blog.datos import posts
from blog.menu import mostrar_menu, pedir_texto
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_todos
```

`validaciones.py` importa de `datos.py` las claves y los estados permitidos. `datos.py` no importa nada, así que no hay imports circulares.
