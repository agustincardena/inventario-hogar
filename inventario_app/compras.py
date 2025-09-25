import json
import os
from inventario import guardar_inventario

COMPRAS_PATH = "data/compras.json"

def cargar_lista_compras():
    if not os.path.exists(COMPRAS_PATH):
        return []
    with open(COMPRAS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_lista_compras(lista):
    with open(COMPRAS_PATH, "w") as f:
        json.dump(lista, f, indent=4)

def generar_lista_compras(inventario, guardar=False):
    lista = [p for p, d in inventario.items() if d["cantidad"] < d["minimo"]]
    if guardar:
        guardar_lista_compras(lista)
    return lista

def mostrar_lista_compras(lista):
    if not lista:
        print("🛍️ La lista de compras está vacía.")
    else:
        print("\n🛒 Lista de compras:")
        for p in lista:
            print(f" - {p}")

def marcar_comprados(inventario):
    lista = cargar_lista_compras()
    if not lista:
        print("🛍️ No hay productos en la lista de compras.")
        return

    print("\nProductos en lista:")
    for i, p in enumerate(lista, start=1):
        print(f"{i}. {p}")

    seleccionados = input("\nNúmeros de productos comprados (separados por coma): ").split(",")

    for num in seleccionados:
        try:
            idx = int(num.strip()) - 1
            if 0 <= idx < len(lista):
                producto = lista[idx]
                cantidad = int(input(f"Cantidad comprada de {producto}: "))
                inventario[producto]["cantidad"] += cantidad
                print(f"✅ {producto} actualizado.")
        except ValueError:
            print("❌ Entrada inválida.")

    guardar_lista_compras([])
    guardar_inventario(inventario)
    print("🛍️ Lista de compras vaciada.")

def eliminar_de_lista_compras(producto):
    lista = cargar_lista_compras()
    producto = producto.lower()
    if producto in lista:
        lista.remove(producto)
        guardar_lista_compras(lista)
