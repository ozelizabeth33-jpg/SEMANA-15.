import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class LoginView:
    def __init__(self, root, servicio, abrir_principal):
        self.root = root
        self.servicio = servicio
        self.abrir_principal = abrir_principal
        self.root.title("Restaurante App - Inicio de sesión")
        self.root.geometry("480x600")
        self.root.resizable(False, False)
        self.logo = None
        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=30)
        contenedor.pack(fill="both", expand=True)

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if ruta_logo.exists():
            self.logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(contenedor, image=self.logo).pack(pady=(0, 8))

        ttk.Label(contenedor, text="RESTAURANTE APP", font=("Arial", 22, "bold")).pack(pady=(0, 5))
        ttk.Label(contenedor, text="Semana 15 · Manejo de eventos").pack(pady=(0, 18))

        formulario = ttk.LabelFrame(contenedor, text="Datos de acceso", padding=20)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Identificación:").grid(row=0, column=0, sticky="w", pady=8)
        self.identificacion = ttk.Entry(formulario)
        self.identificacion.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=8)

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8)
        self.nombre = ttk.Entry(formulario)
        self.nombre.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=8)
        formulario.columnconfigure(1, weight=1)

        ttk.Button(contenedor, text="INGRESAR", command=self.iniciar_sesion).pack(pady=25)
        self.identificacion.focus()

    def iniciar_sesion(self):
        identificacion = self.identificacion.get().strip()
        nombre = self.nombre.get().strip()
        if not identificacion or not nombre:
            messagebox.showwarning("Datos incompletos", "Ingrese la identificación y el nombre.")
            return
        if self.servicio.validar_acceso(identificacion, nombre):
            self.root.destroy()
            self.abrir_principal()
        else:
            messagebox.showerror("Acceso denegado", "La identificación o el nombre son incorrectos.")
