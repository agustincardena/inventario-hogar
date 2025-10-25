import tkinter as tk
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from inventario_app.inventario import abrir_inventario, abrir_lista_compras


def main():
    root = tk.Tk()
    root.title("Gestor de Inventario")
    root.geometry("300x200")

    tk.Label(root, text="Menú Principal", font=("Arial", 14)).pack(pady=20)

    tk.Button(
        root,
        text="Abrir Inventario",
        command=lambda: abrir_inventario(root),
        width=20,
    ).pack(pady=10)

    tk.Button(
        root,
        text="Ver Lista de Compras",
        command=lambda: abrir_lista_compras(root),
        width=20,
    ).pack(pady=10)

    tk.Button(root, text="Salir", command=root.quit, width=20).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
