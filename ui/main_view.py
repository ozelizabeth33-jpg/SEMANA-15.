import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class MainView:
    def __init__(self, root, servicio, cerrar_sesion):
        self.root = root
        self.servicio = servicio
        self.cerrar_sesion = cerrar_sesion
        self.root.title("Restaurante App - Sistema de Gestión")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)
        self.logo = None
        self.icon_venta = None
        self.crear_interfaz()
        self.mostrar_productos()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=15)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 15))

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if ruta_logo.exists():
            self.logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(encabezado, image=self.logo).pack(side="left", padx=(0, 10))

        ttk.Label(encabezado, text="RESTAURANTE APP", font=("Arial", 22, "bold")).pack(side="left")
        ttk.Button(encabezado, text="Cerrar sesión", command=self.cerrar_sesion).pack(side="right")

        navegacion = ttk.LabelFrame(contenedor, text="Secciones", padding=10)
        navegacion.pack(fill="x", pady=(0, 10))
        ttk.Button(navegacion, text="Usuarios", command=self.mostrar_usuarios).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Productos", command=self.mostrar_productos).pack(side="left", padx=5)

        ruta_icon = Path(__file__).resolve().parent.parent / "assets" / "venta.png"
        if ruta_icon.exists():
            self.icon_venta = tk.PhotoImage(file=str(ruta_icon))
        boton_ventas = ttk.Button(navegacion, text="Ventas", image=self.icon_venta, compound="left", command=self.mostrar_ventas)
        boton_ventas.pack(side="left", padx=5)

        self.contenido = ttk.Frame(contenedor)
        self.contenido.pack(fill="both", expand=True)

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_usuarios(self):
        self.limpiar_contenido()
        ttk.Label(self.contenido, text="Consulta de usuarios", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 10))
        contenedor_tabla = ttk.LabelFrame(self.contenido, text="Usuarios registrados", padding=10)
        contenedor_tabla.pack(fill="both", expand=True)
        columnas = ("identificacion", "nombre")
        tabla = ttk.Treeview(contenedor_tabla, columns=columnas, show="headings")
        tabla.heading("identificacion", text="Identificación")
        tabla.heading("nombre", text="Nombre")
        tabla.column("identificacion", width=250)
        tabla.column("nombre", width=300)
        scrollbar = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for usuario in self.servicio.listar_usuarios():
            tabla.insert("", "end", values=(usuario.identificacion, usuario.nombre))

    def mostrar_productos(self):
        self.limpiar_contenido()
        ttk.Label(self.contenido, text="Gestión de productos", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(self.contenido, text="Información del producto", padding=15)
        formulario.pack(fill="x", pady=(0, 10))
        campos = [("Código:", "entry_codigo", 0, 0), ("Nombre:", "entry_nombre", 0, 2), ("Precio:", "entry_precio", 1, 0), ("Stock:", "entry_stock", 1, 2)]
        for texto, atributo, fila, columna in campos:
            ttk.Label(formulario, text=texto).grid(row=fila, column=columna, sticky="w", padx=5, pady=5)
            entrada = ttk.Entry(formulario, width=25)
            entrada.grid(row=fila, column=columna + 1, padx=5, pady=5)
            setattr(self, atributo, entrada)

        botones = ttk.Frame(self.contenido)
        botones.pack(fill="x", pady=(0, 10))
        ttk.Button(botones, text="Registrar", command=self.registrar_producto).pack(side="left", padx=4)
        ttk.Button(botones, text="Cargar / Consultar", command=self.cargar_producto).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=4)

        tabla_contenedor = ttk.LabelFrame(self.contenido, text="Productos registrados", padding=10)
        tabla_contenedor.pack(fill="both", expand=True)
        columnas = ("codigo", "nombre", "precio", "stock")
        self.tabla_productos = ttk.Treeview(tabla_contenedor, columns=columnas, show="headings")
        for col, titulo, ancho in [("codigo", "Código", 120), ("nombre", "Nombre", 250), ("precio", "Precio", 120), ("stock", "Stock", 120)]:
            self.tabla_productos.heading(col, text=titulo)
            self.tabla_productos.column(col, width=ancho)
        scrollbar = ttk.Scrollbar(tabla_contenedor, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        if not hasattr(self, "tabla_productos"):
            return
        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert("", "end", values=(producto.codigo, producto.nombre, f"${producto.precio:.2f}", producto.stock))

    def registrar_producto(self):
        correcto, mensaje = self.servicio.registrar_producto(self.entry_codigo.get(), self.entry_nombre.get(), self.entry_precio.get(), self.entry_stock.get())
        if correcto:
            messagebox.showinfo("Registro", mensaje)
            self.actualizar_tabla(); self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Consulta", "Ingrese el código del producto."); return
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Consulta", "No se encontró el producto."); return
        self.entry_nombre.delete(0, tk.END); self.entry_nombre.insert(0, producto.nombre)
        self.entry_precio.delete(0, tk.END); self.entry_precio.insert(0, producto.precio)
        self.entry_stock.delete(0, tk.END); self.entry_stock.insert(0, producto.stock)

    def actualizar_producto(self):
        correcto, mensaje = self.servicio.actualizar_producto(self.entry_codigo.get(), self.entry_nombre.get(), self.entry_precio.get(), self.entry_stock.get())
        if correcto:
            messagebox.showinfo("Actualización", mensaje); self.actualizar_tabla(); self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Eliminación", "Ingrese el código del producto."); return
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Eliminación", "No se encontró el producto."); return
        if not messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar '{producto.nombre}'?"):
            return
        correcto, mensaje = self.servicio.eliminar_producto(codigo)
        if correcto:
            messagebox.showinfo("Eliminación", mensaje); self.actualizar_tabla(); self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        for entrada in (self.entry_codigo, self.entry_nombre, self.entry_precio, self.entry_stock):
            entrada.delete(0, tk.END)
        self.entry_codigo.focus()

    # VENTAS: acción -> command= -> callback -> servicio -> persistencia -> respuesta visual
    def mostrar_ventas(self):
        self.limpiar_contenido()
        ttk.Label(self.contenido, text="Registro de ventas", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(self.contenido, text="Nueva venta", padding=15)
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        usuarios = [f"{u.identificacion} - {u.nombre}" for u in self.servicio.listar_usuarios()]
        self.combo_usuario = ttk.Combobox(formulario, values=usuarios, state="readonly", width=42)
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(formulario, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        productos = [f"{p.codigo} - {p.nombre}" for p in self.servicio.listar_productos()]
        self.combo_producto = ttk.Combobox(formulario, values=productos, state="readonly", width=42)
        self.combo_producto.grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="w", padx=5, pady=6)
        self.entry_cantidad = ttk.Entry(formulario, width=45)
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=6)

        # IMPORTANTE: command recibe la función, no la ejecuta al crear el botón.
        ttk.Button(formulario, text="Registrar venta", command=self.registrar_venta).grid(row=3, column=1, sticky="w", padx=5, pady=10)

        tabla_contenedor = ttk.LabelFrame(self.contenido, text="Ventas registradas", padding=10)
        tabla_contenedor.pack(fill="both", expand=True)
        columnas = ("usuario", "producto", "cantidad", "fecha")
        self.tabla_ventas = ttk.Treeview(tabla_contenedor, columns=columnas, show="headings")
        for col, titulo, ancho in [("usuario", "Usuario", 210), ("producto", "Producto", 220), ("cantidad", "Cantidad", 90), ("fecha", "Fecha", 180)]:
            self.tabla_ventas.heading(col, text=titulo)
            self.tabla_ventas.column(col, width=ancho)
        scrollbar = ttk.Scrollbar(tabla_contenedor, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.actualizar_tabla_ventas()

    def registrar_venta(self):
        usuario_seleccionado = self.combo_usuario.get().strip()
        producto_seleccionado = self.combo_producto.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not usuario_seleccionado or not producto_seleccionado:
            messagebox.showwarning("Venta", "Seleccione un usuario y un producto.")
            return

        identificacion = usuario_seleccionado.split(" - ", 1)[0]
        codigo_producto = producto_seleccionado.split(" - ", 1)[0]

        correcto, mensaje = self.servicio.registrar_venta(identificacion, codigo_producto, cantidad)
        if correcto:
            messagebox.showinfo("Venta registrada", mensaje)
            self.actualizar_tabla_ventas()
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, "1")
        else:
            messagebox.showerror("Error en la venta", mensaje)

    def actualizar_tabla_ventas(self):
        for elemento in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(elemento)
        for venta in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario(venta.identificacion_usuario)
            producto = self.servicio.buscar_producto(venta.codigo_producto)
            nombre_usuario = usuario.nombre if usuario else venta.identificacion_usuario
            nombre_producto = producto.nombre if producto else venta.codigo_producto
            self.tabla_ventas.insert("", "end", values=(nombre_usuario, nombre_producto, venta.cantidad, venta.fecha or "—"))
