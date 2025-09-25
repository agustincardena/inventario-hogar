def mostrar_menu():
    print("\n--- 🧰 Menú de Inventario ---")
    print("1. Ver inventario")
    print("2. Consumir producto")
    print("3. Generar lista de compras")
    print("4. Agregar producto")
    print("5. Marcar productos comprados")
    print("6. Eliminar producto del inventario")
    print("7. Salir")

def mostrar_inventario(inventario):
    if not inventario:
        print("📦 Inventario vacío.")
        return

    print("\n📦 Inventario actual:")
    for producto, datos in inventario.items():
        print(f" - {producto}: {datos['cantidad']} unidades (mínimo: {datos['minimo']})")
