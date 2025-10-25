import tkinter as tk
from tkinter import messagebox, simpledialog

from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from inventario_app.data_manager import cargar_inventario, guardar_inventario
from inventario_app.inventory_logic import (
    InventarioError,
    agregar_o_actualizar_producto,
    consumir_producto as consumir_producto_logic,
    eliminar_producto as eliminar_producto_logic,
)
from inventario_app.compras import (
    cargar_lista_compras,
    agregar_a_lista,
    marcar_comprado_individual,
    marcar_todos_comprados,
    eliminar_de_lista_compras,
)


def abrir_lista_compras(parent):
    """Abre una ventana para visualizar y administrar la lista de compras."""

    window_compras = tk.Toplevel(parent)
    window_compras.title("Lista de Compras")
    window_compras.geometry("400x400")

    lista_compras_widget = tk.Listbox(window_compras, width=40, height=15)
    lista_compras_widget.pack(pady=10)

    def refrescar_lista():
        lista_compras_widget.delete(0, tk.END)
        for item in cargar_lista_compras():
            lista_compras_widget.insert(tk.END, item)

    refrescar_lista()

    def marcar_individual():
        seleccionado = lista_compras_widget.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto.")
            return

        nombre = lista_compras_widget.get(seleccionado)
        marcar_comprado_individual(nombre)
        refrescar_lista()
        messagebox.showinfo("Hecho", f"'{nombre}' marcado como comprado.")

    def marcar_todos():
        if lista_compras_widget.size() == 0:
            messagebox.showinfo("Lista vacía", "No hay productos para marcar.")
            return

        marcar_todos_comprados()
        refrescar_lista()
        messagebox.showinfo("Hecho", "Todos los productos marcados como comprados.")

    tk.Button(
        window_compras,
        text="Marcar como comprado",
        command=marcar_individual,
    ).pack(pady=5)
    tk.Button(window_compras, text="Marcar todos", command=marcar_todos).pack(pady=5)


def abrir_inventario(root):
    """Abre una ventana separada para gestionar el inventario."""
    window = tk.Toplevel(root)
    window.title("Inventario")
    window.geometry("400x500")

    inventario = cargar_inventario()

    frame = tk.Frame(window)
    frame.pack(pady=10)

    lista = tk.Listbox(frame, width=40, height=15)
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lista.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    lista.config(yscrollcommand=scroll.set)

    def actualizar_lista():
        lista.delete(0, tk.END)
        inv = cargar_inventario()
        for nombre, datos in inv.items():
            cantidad = datos.get("cantidad", 0)
            minimo = datos.get("minimo", 0)
            lista.insert(tk.END, f"{nombre} - Cant: {cantidad} (min {minimo})")

    actualizar_lista()

    # --- AGREGAR PRODUCTO ---
    def agregar_producto():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "Ingresá un nombre de producto.")
            return

        cantidad = entry_cantidad.get().strip()
        minimo = entry_minimo.get().strip()

        if not cantidad.isdigit() or not minimo.isdigit():
            messagebox.showwarning("Atención", "Cantidad y mínimo deben ser números enteros.")
            return

        cantidad = int(cantidad)
        minimo = int(minimo)

        if minimo > cantidad:
            messagebox.showwarning(
                "Atención",
                "El mínimo no puede ser mayor que la cantidad inicial.",
            )
            return

        inv = cargar_inventario()
        try:
            mensaje, _ = agregar_o_actualizar_producto(inv, nombre, cantidad, minimo)
        except InventarioError as exc:
            messagebox.showerror("Error", str(exc))
            return

        guardar_inventario(inv)
        actualizar_lista()
        messagebox.showinfo("Éxito", mensaje)
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_minimo.delete(0, tk.END)

    # --- CONSUMIR PRODUCTO ---
    def consumir_producto():
        seleccionado = lista.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto para consumir.")
            return

        item_text = lista.get(seleccionado)
        nombre = item_text.split(" - ")[0]

        cantidad = simpledialog.askinteger(
            "Consumir",
            f"¿Cuántas unidades de '{nombre}' querés consumir?",
            minvalue=1,
            parent=window,
        )
        if cantidad is None:
            return

        inv = cargar_inventario()
        try:
            mensaje = consumir_producto_logic(inv, nombre, cantidad)
        except InventarioError as exc:
            messagebox.showerror("Error", str(exc))
            return

        guardar_inventario(inv)
        actualizar_lista()
        messagebox.showinfo("Éxito", mensaje)

    # --- ELIMINAR PRODUCTO ---
    def eliminar_producto():
        seleccionado = lista.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto para eliminar.")
            return

        item_text = lista.get(seleccionado)
        nombre = item_text.split(" - ")[0]

        inv = cargar_inventario()
        try:
            mensaje = eliminar_producto_logic(inv, nombre)
        except InventarioError as exc:
            messagebox.showerror("Error", str(exc))
            return

        guardar_inventario(inv)
        eliminar_de_lista_compras(nombre.lower())
        actualizar_lista()
        messagebox.showinfo("Eliminado", mensaje)

    # --- ABRIR LISTA DE COMPRAS ---
    def abrir_lista_compras():
        """Abre una ventana para gestionar la lista de compras."""
        window_compras = tk.Toplevel(window)
        window_compras.title("Lista de Compras")
        window_compras.geometry("400x400")

        lista_compras = tk.Listbox(window_compras, width=40, height=15)
        lista_compras.pack(pady=10)

        compras = cargar_lista_compras()
        for item in compras:
            lista_compras.insert(tk.END, item)

        def marcar_individual():
            seleccionado = lista_compras.curselection()
            if not seleccionado:
                messagebox.showwarning("Atención", "Seleccioná un producto.")
                return
            nombre = lista_compras.get(seleccionado)
            marcar_comprado_individual(nombre)
            lista_compras.delete(seleccionado)
            messagebox.showinfo("Hecho", f"'{nombre}' marcado como comprado.")

        def marcar_todos():
            marcar_todos_comprados()
            lista_compras.delete(0, tk.END)
            messagebox.showinfo("Hecho", "Todos los productos marcados como comprados.")

        tk.Button(window_compras, text="Marcar como comprado", command=marcar_individual).pack(pady=5)
        tk.Button(window_compras, text="Marcar todos", command=marcar_todos).pack(pady=5)

    # --- ENTRADAS Y BOTONES ---
    tk.Label(window, text="Producto:").pack()
    entry_nombre = tk.Entry(window, width=25)
    entry_nombre.pack()

    tk.Label(window, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(window, width=10)
    entry_cantidad.pack()

    tk.Label(window, text="Mínimo:").pack()
    entry_minimo = tk.Entry(window, width=10)
    entry_minimo.pack()

    tk.Button(window, text="Agregar/Actualizar", command=agregar_producto, width=20).pack(pady=5)
    tk.Button(window, text="Consumir", command=consumir_producto, width=20).pack(pady=5)
    tk.Button(window, text="Eliminar", command=eliminar_producto, width=20).pack(pady=5)
    tk.Button(
        window,
        text="Ver lista de compras",
        command=lambda: abrir_lista_compras(window),
        width=20,
    ).pack(pady=5)
