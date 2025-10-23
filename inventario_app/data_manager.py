import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INVENTARIO_PATH = os.path.join(DATA_DIR, "inventario.json")
COMPRAS_PATH = os.path.join(DATA_DIR, "compras.json")


def cargar_inventario():
    """Carga el inventario desde el archivo JSON."""
    if not os.path.exists(INVENTARIO_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(INVENTARIO_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        return {}

    with open(INVENTARIO_PATH, "r", encoding="utf-8") as f:
        data = f.read().strip()
        return json.loads(data) if data else {}


def guardar_inventario(inventario):
    """Guarda el inventario en el archivo JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTARIO_PATH, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


def cargar_lista_compras():
    """Carga la lista de compras."""
    if not os.path.exists(COMPRAS_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(COMPRAS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []

    with open(COMPRAS_PATH, "r", encoding="utf-8") as f:
        data = f.read().strip()
        return json.loads(data) if data else []


def guardar_lista_compras(lista):
    """Guarda la lista de compras."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(COMPRAS_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
