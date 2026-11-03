# Todo lo que tiene que ver con hablar con el usuario: el menu y los input().


def mostrar_menu():
    # Muestra el menu y devuelve la opcion como numero (o None si no es un numero)
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")
    try:
        opcion = int(input("Elegi una opcion: "))
        return opcion
    except ValueError:
        print("Error: tenes que escribir un numero del 1 al 5")
        return None


def pedir_texto(mensaje):
    # Pide un texto al usuario y lo devuelve sin espacios al principio ni al final
    texto = input(mensaje).strip()
    return texto
