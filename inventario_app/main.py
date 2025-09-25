from inventario import (
    cargar_inventario,
    guardar_inventario,
    consumir_producto,
    agregar_o_actualizar_producto,
    eliminar_producto
)
from compras import (
    generar_lista_compras,
    mostrar_lista_compras,
    marcar_comprados,
    guardar_lista_compras,
    eliminar_de_lista_compras
)
from utils import mostrar_inventario, mostrar_menu

def main():
    inventario = cargar_inventario()
    
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            mostrar_inventario(inventario)

        elif opcion == "2":
            producto = input("Nombre del producto: ")
            cantidad = int(input("Cantidad a consumir: "))
            consumir_producto(inventario, producto, cantidad)
            guardar_inventario(inventario)

        elif opcion == "3":
            lista = generar_lista_compras(inventario, guardar=True)
            mostrar_lista_compras(lista)
            print("\n¿Querés dejar la lista guardada en blanco?")
            print("1. Sí (vaciar lista)")
            print("2. No (dejarla como está)")
            opcion_lista = input("Elige: ")
            if opcion_lista == "1":
                guardar_lista_compras([])
                print("✅ Lista de compras vaciada.")

        elif opcion == "4":
            producto = input("Nombre del producto: ")
            cantidad = int(input("Cantidad a agregar: "))
            agregar_o_actualizar_producto(inventario, producto, cantidad)
            guardar_inventario(inventario)

        elif opcion == "5":
            marcar_comprados(inventario)

        elif opcion == "6":
            if not inventario:
                print("⚠️ El inventario está vacío.")
                continue

            print("\n--- Productos disponibles ---")
            productos = list(inventario.keys())
            for i, p in enumerate(productos, start=1):
                print(f"{i}. {p} ({inventario[p]['cantidad']} unidades)")

            try:
                seleccion = int(input("\nElige el número del producto a eliminar (0 para cancelar): "))
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            if seleccion == 0:
                print("Operación cancelada.")
                continue

            if 1 <= seleccion <= len(productos):
                producto_a_eliminar = productos[seleccion - 1]
                eliminar_producto(inventario, producto_a_eliminar)
                eliminar_de_lista_compras(producto_a_eliminar)
                guardar_inventario(inventario)
            else:
                print("❌ Número fuera de rango.")

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
