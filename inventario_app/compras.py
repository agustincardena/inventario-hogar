import json
import os
from data_manager import guardar_inventario, cargar_inventario

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
COMPRAS_PATH = os.path.join(DATA_DIR, "compras.json")


def cargar_lista_compras():
    """Carga la lista de compras desde el archivo JSON (si no existe, crea una vacía)."""
    if not os.path.exists(COMPRAS_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(COMPRAS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []
    try:
        with open(COMPRAS_PATH, "r", encoding="utf-8") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        return []


def guardar_lista_compras(lista):
    """Guarda la lista de compras en el archivo JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(COMPRAS_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


def agregar_a_lista(nombre):
    """Agrega un producto a la lista de compras si no está ya."""
    lista = cargar_lista_compras()
    nombre = nombre.lower()

    if nombre not in lista:
        lista.append(nombre)
        guardar_lista_compras(lista)
        print(f"'{nombre}' agregado a la lista de compras.")
    else:
        print(f"'{nombre}' ya está en la lista de compras.")


def marcar_comprado_individual(nombre):
    """Marca un producto individual como comprado y lo repone al mínimo."""
    inventario = cargar_inventario()
    lista = cargar_lista_compras()

    nombre = nombre.lower()
    if nombre in lista:
        lista.remove(nombre)
    if nombre in inventario:
        minimo = inventario[nombre].get("minimo", 1)
        inventario[nombre]["cantidad"] = minimo
    else:
        inventario[nombre] = {"cantidad": 1, "minimo": 1}

    guardar_inventario(inventario)
    guardar_lista_compras(lista)


def marcar_todos_comprados():
    """Marca todos los productos como comprados."""
    inventario = cargar_inventario()
    lista = cargar_lista_compras()

    for nombre in lista:
        if nombre in inventario:
            minimo = inventario[nombre].get("minimo", 1)
            inventario[nombre]["cantidad"] = minimo
        else:
            inventario[nombre] = {"cantidad": 1, "minimo": 1}

    guardar_inventario(inventario)
    guardar_lista_compras([])  # Limpia la lista después
