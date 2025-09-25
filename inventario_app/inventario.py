import json
import os

DATA_PATH = "data/inventario.json"

def cargar_inventario():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        try:
            data = json.load(f)
            # 🔎 Normalizamos todas las claves a minúsculas
            inventario_normalizado = {
                k.lower(): v for k, v in data.items()
            }
            return inventario_normalizado
        except json.JSONDecodeError:
            return {}


def guardar_inventario(inventario):
    with open(DATA_PATH, "w") as f:
        json.dump(inventario, f, indent=4)

def consumir_producto(inventario, producto, cantidad):
    producto = producto.lower()
    if producto in inventario:
        inventario[producto]["cantidad"] -= cantidad
        if inventario[producto]["cantidad"] < 0:
            inventario[producto]["cantidad"] = 0
        print(f"✅ {cantidad} unidades de {producto} consumidas.")
    else:
        print("❌ El producto no existe en el inventario.")

def agregar_o_actualizar_producto(inventario, producto, cantidad):
    producto = producto.lower()
    if producto in inventario:
        inventario[producto]["cantidad"] += cantidad
        print(f"📦 Se agregaron {cantidad} unidades a {producto}.")
    else:
        minimo = int(input(f"Cantidad mínima deseada para {producto}: "))
        inventario[producto] = {"cantidad": cantidad, "minimo": minimo}
        print(f"✅ Producto {producto} agregado al inventario.")

def eliminar_producto(inventario, producto):
    producto = producto.lower()
    if producto in inventario:
        del inventario[producto]
        print(f"🗑️  {producto} eliminado del inventario.")
    else:
        print("❌ El producto no existe.")
