"""Operaciones relacionadas con la lista de compras."""
from __future__ import annotations

from typing import List, Sequence

from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from inventario_app.data_manager import (
    cargar_inventario,
    cargar_lista_compras as _cargar_lista_compras,
    guardar_inventario,
    guardar_lista_compras as _guardar_lista_compras,
)


def cargar_lista_compras() -> List[str]:
    """Carga la lista de compras desde disco."""

    return _cargar_lista_compras()


def guardar_lista_compras(lista: Sequence[str]) -> None:
    """Persiste la lista de compras."""

    _guardar_lista_compras(list(lista))


def agregar_a_lista(nombre: str) -> None:
    """Agrega un producto a la lista de compras si no está ya."""

    lista = cargar_lista_compras()
    nombre = nombre.lower()

    if nombre not in lista:
        lista.append(nombre)
        guardar_lista_compras(lista)
        print(f"'{nombre}' agregado a la lista de compras.")
    else:
        print(f"'{nombre}' ya está en la lista de compras.")


def marcar_comprado_individual(nombre: str) -> None:
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


def marcar_todos_comprados() -> None:
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
    guardar_lista_compras([])


def eliminar_de_lista_compras(nombre: str) -> bool:
    """Elimina un producto de la lista de compras."""

    lista = cargar_lista_compras()
    nombre = nombre.lower()
    if nombre in lista:
        lista.remove(nombre)
        guardar_lista_compras(lista)
        return True
    return False


def generar_lista_compras(inventario, guardar: bool = False):
    """Genera una lista con los productos debajo de su mínimo."""

    lista = []
    for nombre, datos in inventario.items():
        minimo = datos.get("minimo", 0)
        cantidad = datos.get("cantidad", 0)
        if cantidad <= minimo:
            lista.append(nombre)

    if guardar:
        guardar_lista_compras(lista)
    return lista


def mostrar_lista_compras(lista):
    """Muestra en consola la lista de compras."""

    if not lista:
        print("🛒 La lista de compras está vacía.")
        return

    print("\n🛒 Lista de compras:")
    for i, item in enumerate(lista, start=1):
        print(f" {i}. {item}")


def marcar_comprados(_inventario):
    """Permite marcar artículos como comprados desde la consola."""

    lista = cargar_lista_compras()
    if not lista:
        print("🛒 No hay productos pendientes en la lista de compras.")
        return

    while True:
        mostrar_lista_compras(lista)
        print("\nOpciones:")
        print(" 0. Volver al menú")
        print(" a. Marcar todos")
        seleccion = input("Seleccioná un número o 'a': ").strip().lower()

        if seleccion == "0":
            break
        if seleccion == "a":
            marcar_todos_comprados()
            print("✅ Todos los productos fueron marcados como comprados.")
            lista = []
            break

        if not seleccion.isdigit():
            print("❌ Selección inválida.")
            continue

        indice = int(seleccion) - 1
        if 0 <= indice < len(lista):
            producto = lista[indice]
            marcar_comprado_individual(producto)
            print(f"✅ '{producto}' marcado como comprado.")
            lista = cargar_lista_compras()
            if not lista:
                print("🛒 No quedan productos en la lista de compras.")
                break
        else:
            print("❌ Número fuera de rango.")
