"""Funciones reutilizables para operar sobre el inventario.

Estas rutinas encapsulan validaciones compartidas por la interfaz
gráfica y la interfaz de línea de comandos.
"""
from __future__ import annotations

from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import Dict, Tuple

from inventario_app.compras import agregar_a_lista

Inventory = Dict[str, Dict[str, int]]


class InventarioError(ValueError):
    """Errores relacionados con operaciones del inventario."""


def _normalizar_nombre(nombre: str) -> str:
    nombre_normalizado = nombre.strip().lower()
    if not nombre_normalizado:
        raise InventarioError("El nombre del producto no puede estar vacío.")
    return nombre_normalizado


def agregar_o_actualizar_producto(
    inventario: Inventory,
    nombre: str,
    cantidad: int,
    minimo: int | None = None,
) -> Tuple[str, bool]:
    """Agrega un producto nuevo o actualiza uno existente.

    Devuelve una tupla con un mensaje para el usuario y un indicador
    que especifica si el producto fue creado (``True``) o simplemente
    actualizado (``False``).
    """

    nombre_normalizado = _normalizar_nombre(nombre)

    if cantidad <= 0:
        raise InventarioError("La cantidad debe ser mayor que cero.")

    if minimo is not None and minimo <= 0:
        raise InventarioError("El mínimo debe ser mayor que cero.")

    if nombre_normalizado in inventario:
        producto = inventario[nombre_normalizado]
        producto["cantidad"] += cantidad
        if minimo is not None:
            if minimo > producto["cantidad"]:
                raise InventarioError(
                    "El mínimo no puede ser mayor que la cantidad actual."
                )
            producto["minimo"] = minimo
        return f"'{nombre_normalizado}' actualizado correctamente.", False

    if minimo is None:
        raise InventarioError(
            "Debés indicar un mínimo para registrar un nuevo producto."
        )

    if minimo > cantidad:
        raise InventarioError("El mínimo no puede ser mayor que la cantidad inicial.")

    inventario[nombre_normalizado] = {"cantidad": cantidad, "minimo": minimo}
    return f"'{nombre_normalizado}' agregado al inventario.", True


def consumir_producto(inventario: Inventory, nombre: str, cantidad: int) -> str:
    """Descuenta unidades de un producto existente.

    Si el stock queda por debajo del mínimo, agrega el producto a la lista de
    compras automáticamente.
    """

    nombre_normalizado = _normalizar_nombre(nombre)

    if cantidad <= 0:
        raise InventarioError("La cantidad a consumir debe ser mayor que cero.")

    if nombre_normalizado not in inventario:
        raise InventarioError(f"El producto '{nombre_normalizado}' no existe en el inventario.")

    producto = inventario[nombre_normalizado]
    if cantidad > producto["cantidad"]:
        raise InventarioError(
            f"No hay stock suficiente de '{nombre_normalizado}' para consumir {cantidad} unidades."
        )

    producto["cantidad"] -= cantidad

    if producto["cantidad"] <= producto.get("minimo", 0):
        agregar_a_lista(nombre_normalizado)

    return (
        f"Consumidas {cantidad} unidad(es) de '{nombre_normalizado}'. "
        f"Stock restante: {producto['cantidad']}."
    )


def eliminar_producto(inventario: Inventory, nombre: str) -> str:
    """Elimina un producto del inventario."""

    nombre_normalizado = _normalizar_nombre(nombre)
    if nombre_normalizado not in inventario:
        raise InventarioError(f"El producto '{nombre_normalizado}' no está en el inventario.")

    del inventario[nombre_normalizado]
    return f"'{nombre_normalizado}' fue eliminado del inventario."
