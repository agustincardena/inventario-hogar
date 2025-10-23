import tkinter as tk
from tkinter import messagebox
from data_manager import cargar_inventario, guardar_inventario
from compras import (
    cargar_lista_compras,
    agregar_a_lista,
    marcar_comprado_individual,
    marcar_todos_comprados,
)


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
        nombre = entry_nombre.get().strip().lower()
        if not nombre:
            messagebox.showwarning("Atención", "Ingresá un nombre de producto.")
            return

        cantidad = entry_cantidad.get().strip()
        minimo = entry_minimo.get().strip()

        if not cantidad.isdigit() or not minimo.isdigit():
            messagebox.showwarning("Atención", "Cantidad y mínimo deben ser números.")
            return

        cantidad = int(cantidad)
        minimo = int(minimo)
        inv = cargar_inventario()

        if nombre in inv:
            inv[nombre]["cantidad"] += cantidad
        else:
            inv[nombre] = {"cantidad": cantidad, "minimo": minimo}

        guardar_inventario(inv)
        actualizar_lista()
        messagebox.showinfo("Éxito", f"'{nombre}' agregado o actualizado.")
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
        nombre = item_text.split(" - ")[0].lower()

        inv = cargar_inventario()
        if nombre not in inv:
            messagebox.showerror("Error", "El producto no existe.")
            return

        if inv[nombre]["cantidad"] > 0:
            inv[nombre]["cantidad"] -= 1
            if inv[nombre]["cantidad"] <= inv[nombre]["minimo"]:
                agregar_a_lista(nombre)
            guardar_inventario(inv)
            actualizar_lista()
        else:
            messagebox.showinfo("Aviso", f"'{nombre}' ya no tiene stock.")

    # --- ELIMINAR PRODUCTO ---
    def eliminar_producto():
        seleccionado = lista.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un producto para eliminar.")
            return

        item_text = lista.get(seleccionado)
        nombre = item_text.split(" - ")[0].lower()

        inv = cargar_inventario()
        if nombre in inv:
            del inv[nombre]
            guardar_inventario(inv)
            actualizar_lista()
            messagebox.showinfo("Eliminado", f"'{nombre}' fue eliminado del inventario.")

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
    tk.Button(window, text="Ver lista de compras", command=abrir_lista_compras, width=20).pack(pady=5)
