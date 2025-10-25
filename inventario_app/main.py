"""Interfaz de línea de comandos para el inventario."""
from __future__ import annotations

from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from inventario_app.data_manager import cargar_inventario, guardar_inventario
from inventario_app.inventory_logic import (
    InventarioError,
    agregar_o_actualizar_producto,
    consumir_producto,
    eliminar_producto,
)
from inventario_app.compras import (
    generar_lista_compras,
    mostrar_lista_compras,
    marcar_comprados,
    guardar_lista_compras,
    eliminar_de_lista_compras,
)
from inventario_app.utils import mostrar_inventario, mostrar_menu


def solicitar_entero(mensaje: str) -> int:
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("❌ Tenés que ingresar un número.")
            continue
        if not valor.isdigit():
            print("❌ Ingresá solo números enteros positivos.")
            continue
        numero = int(valor)
        if numero <= 0:
            print("❌ El número debe ser mayor a cero.")
            continue
        return numero


def main() -> None:
    inventario = cargar_inventario()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_inventario(inventario)

        elif opcion == "2":
            producto = input("Nombre del producto: ").strip()
            if not producto:
                print("❌ Debés ingresar un nombre de producto.")
                continue
            cantidad = solicitar_entero("Cantidad a consumir: ")
            try:
                mensaje = consumir_producto(inventario, producto, cantidad)
            except InventarioError as exc:
                print(f"❌ {exc}")
                continue
            guardar_inventario(inventario)
            inventario = cargar_inventario()
            print(f"✅ {mensaje}")

        elif opcion == "3":
            lista = generar_lista_compras(inventario, guardar=True)
            mostrar_lista_compras(lista)
            print("\n¿Querés dejar la lista guardada en blanco?")
            print("1. Sí (vaciar lista)")
            print("2. No (dejarla como está)")
            opcion_lista = input("Elige: ").strip()
            if opcion_lista == "1":
                guardar_lista_compras([])
                print("✅ Lista de compras vaciada.")

        elif opcion == "4":
            producto = input("Nombre del producto: ").strip()
            if not producto:
                print("❌ Debés ingresar un nombre de producto.")
                continue
            cantidad = solicitar_entero("Cantidad a agregar: ")
            minimo_raw = input(
                "Mínimo deseado (dejar en blanco para mantener el actual): "
            ).strip()
            minimo = None
            if minimo_raw:
                if not minimo_raw.isdigit():
                    print("❌ El mínimo debe ser un número entero positivo.")
                    continue
                minimo = int(minimo_raw)
            try:
                mensaje, _ = agregar_o_actualizar_producto(
                    inventario, producto, cantidad, minimo
                )
            except InventarioError as exc:
                print(f"❌ {exc}")
                continue
            guardar_inventario(inventario)
            inventario = cargar_inventario()
            print(f"✅ {mensaje}")

        elif opcion == "5":
            marcar_comprados(inventario)
            inventario = cargar_inventario()

        elif opcion == "6":
            if not inventario:
                print("⚠️ El inventario está vacío.")
                continue

            print("\n--- Productos disponibles ---")
            productos = list(inventario.keys())
            for i, p in enumerate(productos, start=1):
                cantidad = inventario[p]["cantidad"]
                print(f"{i}. {p} ({cantidad} unidades)")

            seleccion = input(
                "\nElige el número del producto a eliminar (0 para cancelar): "
            ).strip()
            if not seleccion.isdigit():
                print("❌ Entrada inválida.")
                continue

            seleccion_num = int(seleccion)
            if seleccion_num == 0:
                print("Operación cancelada.")
                continue

            if 1 <= seleccion_num <= len(productos):
                producto_a_eliminar = productos[seleccion_num - 1]
                try:
                    mensaje = eliminar_producto(inventario, producto_a_eliminar)
                except InventarioError as exc:
                    print(f"❌ {exc}")
                    continue
                eliminar_de_lista_compras(producto_a_eliminar)
                guardar_inventario(inventario)
                inventario = cargar_inventario()
                print(f"✅ {mensaje}")
            else:
                print("❌ Número fuera de rango.")

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
