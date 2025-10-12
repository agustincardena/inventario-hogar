import json
import os

DATA_DIR = "data"
INVENTARIO_PATH = os.path.join(DATA_DIR, "inventario.json")

# ===============================
#   FUNCIONES PRINCIPALES
# ===============================

def cargar_inventario():
    """Carga el inventario desde el archivo JSON (si no existe, devuelve uno vacío)."""
    if not os.path.exists(INVENTARIO_PATH):
        return {}

    try:
        with open(INVENTARIO_PATH, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return {}
            inventario = json.loads(data)
            # Normalizamos las claves a minúsculas
            return {k.lower(): v for k, v in inventario.items()}
    except json.JSONDecodeError:
        return {}


def guardar_inventario(inventario):
    """Guarda el inventario en el archivo JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTARIO_PATH, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)


def agregar_producto(nombre, cantidad, minimo):
    """Agrega un producto nuevo al inventario o lo actualiza si ya existe."""
    from compras import guardar_lista_compras  # Evita import circular
    inventario = cargar_inventario()
    nombre = nombre.lower()

    inventario[nombre] = {"cantidad": cantidad, "minimo": minimo}
    guardar_inventario(inventario)


def eliminar_producto(nombre):
    """Elimina un producto del inventario."""
    inventario = cargar_inventario()
    nombre = nombre.lower()

    if nombre in inventario:
        del inventario[nombre]
        guardar_inventario(inventario)
        print(f"'{nombre}' eliminado del inventario.")
    else:
        print(f"'{nombre}' no existe en el inventario.")


def consumir_producto(nombre, cantidad):
    """Reduce la cantidad de un producto y, si baja del mínimo, lo agrega a la lista de compras."""
    from compras import agregar_a_lista

    inventario = cargar_inventario()
    nombre = nombre.lower()

    if nombre not in inventario:
        print(f"El producto '{nombre}' no está en el inventario.")
        return

    inventario[nombre]["cantidad"] -= cantidad
    if inventario[nombre]["cantidad"] < 0:
        inventario[nombre]["cantidad"] = 0

    guardar_inventario(inventario)

    # Si está por debajo del mínimo, lo manda a la lista de compras
    if inventario[nombre]["cantidad"] < inventario[nombre]["minimo"]:
        agregar_a_lista(nombre)
