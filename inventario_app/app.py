import tkinter as tk
from tkinter import messagebox
from inventario import cargar_inventario, guardar_inventario
from compras import cargar_lista_compras, agregar_a_lista, marcar_comprados

# ========================
# CONFIGURACIÓN DE LA VENTANA
# ========================
root = tk.Tk()
root.title("Inventario del Hogar ")
root.geometry("400x500")
root.config(bg="#f7f9fc")

# ========================
# ESTILOS
# ========================
BTN_COLOR = "#C6AD86"
BTN_HOVER = "#B5946A"
BTN_TEXT = "white"
FRAME_BG = "#F2F3D9"
FONT_MAIN = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 14, "bold")

# ========================
# FUNCIONES AUXILIARES
# ========================
def hover_on(e):
    e.widget.config(bg=BTN_HOVER)

def hover_off(e):
    e.widget.config(bg=BTN_COLOR)

def crear_boton(master, text, command):
    btn = tk.Button(
        master,
        text=text,
        command=command,
        bg=BTN_COLOR,
        fg=BTN_TEXT,
        font=FONT_MAIN,
        relief="flat",
        bd=0,
        highlightthickness=0,
        padx=6,
        pady=4,
        cursor="hand2",
    )
    btn.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off)
    return btn

# ========================
# FUNCIONES DE INTERFAZ
# ========================
def mostrar_inventario():
    inventario = cargar_inventario()
    if not inventario:
        messagebox.showinfo("Inventario", "No hay productos cargados.")
        return
    texto = "\n".join([f"{k}: {v['cantidad']} (mínimo: {v['minimo']})" for k, v in inventario.items()])
    messagebox.showinfo("Inventario actual", texto)

def simple_input(prompt):
    win = tk.Toplevel(root)
    win.title("Entrada requerida")
    win.geometry("260x130")
    win.config(bg="#f7f9fc")

    tk.Label(win, text=prompt, bg="#f7f9fc", font=FONT_MAIN).pack(pady=8)
    entry = tk.Entry(win, font=FONT_MAIN, width=22)
    entry.pack(pady=4)

    value = tk.StringVar()
    def confirmar():
        value.set(entry.get())
        win.destroy()
    crear_boton(win, "Aceptar", confirmar).pack(pady=8)

    win.wait_window()
    return value.get()

def agregar_producto_ui():
    nombre = entry_nombre.get().strip().lower()
    cantidad = entry_cantidad.get().strip()

    if not nombre or not cantidad.isdigit():
        messagebox.showwarning("Error", "Ingrese un nombre y cantidad válida.")
        return

    cantidad = int(cantidad)
    inventario = cargar_inventario()
    if nombre in inventario:
        inventario[nombre]["cantidad"] += cantidad
    else:
        cantidad_minima = simple_input("Cantidad mínima deseada:")
        if not cantidad_minima.isdigit():
            messagebox.showwarning("Error", "Ingrese una cantidad mínima válida.")
            return
        inventario[nombre] = {"cantidad": cantidad, "minimo": int(cantidad_minima)}

    guardar_inventario(inventario)
    messagebox.showinfo("Éxito", f"{nombre} agregado/actualizado correctamente.")
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

def consumir_producto_ui():
    inventario = cargar_inventario()
    productos_validos = [p for p, info in inventario.items() if info["cantidad"] > 0]

    if not productos_validos:
        messagebox.showinfo("Info", "No hay productos disponibles para consumir.")
        return

    win = tk.Toplevel(root)
    win.title("Consumir producto")
    win.geometry("260x200")
    win.config(bg="#f7f9fc")

    tk.Label(win, text="Seleccione el producto:", bg="#f7f9fc", font=FONT_MAIN).pack(pady=8)
    var = tk.StringVar(value=productos_validos[0])
    lista = tk.OptionMenu(win, var, *productos_validos)
    lista.config(font=FONT_MAIN, bg="#ffffff", relief="flat")
    lista.pack(pady=8)

    def confirmar():
        producto = var.get()
        inventario[producto]["cantidad"] -= 1
        if inventario[producto]["cantidad"] <= 0:
            agregar_a_lista(producto)
        guardar_inventario(inventario)
        messagebox.showinfo("Éxito", f"Se consumió una unidad de {producto}.")
        win.destroy()

    crear_boton(win, "Consumir", confirmar).pack(pady=8)

def eliminar_producto_ui():
    inventario = cargar_inventario()
    if not inventario:
        messagebox.showinfo("Info", "No hay productos para eliminar.")
        return

    win = tk.Toplevel(root)
    win.title("Eliminar producto")
    win.geometry("260x200")
    win.config(bg="#f7f9fc")

    tk.Label(win, text="Seleccione el producto:", bg="#f7f9fc", font=FONT_MAIN).pack(pady=8)
    var = tk.StringVar(value=list(inventario.keys())[0])
    lista = tk.OptionMenu(win, var, *inventario.keys())
    lista.config(font=FONT_MAIN, bg="#ffffff", relief="flat")
    lista.pack(pady=8)

    def confirmar():
        producto = var.get()
        del inventario[producto]
        guardar_inventario(inventario)
        messagebox.showinfo("Éxito", f"Producto '{producto}' eliminado.")
        win.destroy()

    crear_boton(win, "Eliminar", confirmar).pack(pady=8)

def marcar_comprados_ui():
    inventario = cargar_inventario()
    marcar_comprados(inventario)

def mostrar_lista_compras():
    lista = cargar_lista_compras()
    if not lista:
        messagebox.showinfo("Lista de compras", "No hay productos para comprar.")
        return
    texto = "\n".join(lista)
    messagebox.showinfo("🛒 Lista de compras", texto)

# ========================
# FRAME PRINCIPAL
# ========================
frame = tk.Frame(root, bg=FRAME_BG, bd=2, relief="groove")
frame.pack(fill="both", expand=True, padx=10, pady=10)

titulo = tk.Label(frame, text="Inventario del Hogar", font=FONT_TITLE, bg=FRAME_BG, fg="#333")
titulo.pack(pady=6)

# ENTRADAS
tk.Label(frame, text="Producto:", bg=FRAME_BG, font=FONT_MAIN).pack(pady=(8, 0))
entry_nombre = tk.Entry(frame, font=FONT_MAIN, width=25)
entry_nombre.pack(pady=4)

tk.Label(frame, text="Cantidad:", bg=FRAME_BG, font=FONT_MAIN).pack(pady=(8, 0))
entry_cantidad = tk.Entry(frame, font=FONT_MAIN, width=25)
entry_cantidad.pack(pady=4)

crear_boton(frame, "Agregar producto", agregar_producto_ui).pack(pady=6)
crear_boton(frame, "Consumir producto", consumir_producto_ui).pack(pady=4)
crear_boton(frame, "Eliminar producto", eliminar_producto_ui).pack(pady=4)
crear_boton(frame, "Ver inventario", mostrar_inventario).pack(pady=4)
crear_boton(frame, "Ver lista de compras", mostrar_lista_compras).pack(pady=4)
crear_boton(frame, "Marcar comprados", marcar_comprados_ui).pack(pady=4)

root.mainloop()
