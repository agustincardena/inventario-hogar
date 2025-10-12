import os
import json
from tkinter import messagebox
from inventario import guardar_inventario

DATA_DIR = "data"
COMPRAS_PATH = os.path.join(DATA_DIR, "compras.json")

def cargar_lista_compras():
    """Carga la lista de compras desde el archivo JSON (si no existe, crea una vacía)."""
    if not os.path.exists(COMPRAS_PATH):
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
        messagebox.showinfo("Lista de Compras", f"🛒 '{nombre}' agregado a la lista de compras.")
    else:
        messagebox.showinfo("Lista de Compras", f"'{nombre}' ya está en la lista de compras.")

def marcar_comprados(inventario):
    """Marca los productos como comprados, los repone en el inventario y limpia la lista."""
    lista = cargar_lista_compras()
    if not lista:
        messagebox.showinfo("Lista de Compras", "No hay productos en la lista de compras.")
        return

    for producto in lista:
        if producto not in inventario:
            inventario[producto] = {"cantidad": 1, "minimo": 1}
        else:
            minimo = inventario[producto]["minimo"]
            inventario[producto]["cantidad"] = minimo

    guardar_inventario(inventario)
    guardar_lista_compras([])
    messagebox.showinfo("Éxito", "✅ Lista de compras vaciada y productos repuestos en inventario.")
