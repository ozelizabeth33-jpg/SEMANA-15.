from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        self.usuarios = [
            Usuario(d.get("identificacion", ""), d.get("nombre", ""))
            for d in ArchivoServicio.leer_json("usuarios.json")
        ]
        self.productos = [
            Producto(
                d.get("codigo", ""),
                d.get("nombre", ""),
                d.get("precio", 0),
                d.get("stock", 0),
            )
            for d in ArchivoServicio.leer_json("productos.json")
        ]
        self.ventas = [
            Venta(
                d.get("identificacion_usuario", ""),
                d.get("codigo_producto", ""),
                d.get("cantidad", 1),
                d.get("fecha", ""),
            )
            for d in ArchivoServicio.leer_json("ventas.json")
        ]

    # LOGIN
    def validar_acceso(self, identificacion, nombre):
        for usuario in self.usuarios:
            if (
                usuario.identificacion == identificacion
                and usuario.nombre.strip().lower() == nombre.strip().lower()
            ):
                return True
        return False

    # USUARIOS
    def listar_usuarios(self):
        return self.usuarios

    def buscar_usuario(self, identificacion):
        for usuario in self.usuarios:
            if usuario.identificacion.strip().lower() == identificacion.strip().lower():
                return usuario
        return None

    # PRODUCTOS
    def listar_productos(self):
        return self.productos

    def buscar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo.strip().lower() == codigo.strip().lower():
                return producto
        return None

    def registrar_producto(self, codigo, nombre, precio, stock):
        codigo = codigo.strip()
        nombre = nombre.strip()
        if not codigo:
            return False, "El código es obligatorio."
        if not nombre:
            return False, "El nombre es obligatorio."
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return False, "Precio y stock deben ser valores numéricos."
        if precio < 0 or stock < 0:
            return False, "Precio y stock no pueden ser negativos."
        if self.buscar_producto(codigo):
            return False, "Ya existe un producto con ese código."
        self.productos.append(Producto(codigo, nombre, precio, stock))
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, codigo, nombre, precio, stock):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "No se encontró el producto."
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return False, "Precio y stock deben ser valores numéricos."
        if precio < 0 or stock < 0:
            return False, "Precio y stock no pueden ser negativos."
        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        self.guardar_productos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "No se encontró el producto."
        self.productos.remove(producto)
        self.guardar_productos()
        return True, "Producto eliminado correctamente."

    def guardar_productos(self):
        ArchivoServicio.guardar_json(
            "productos.json", [producto.to_dict() for producto in self.productos]
        )

    # VENTAS - SEMANA 15
    def listar_ventas(self):
        return self.ventas

    def registrar_venta(self, identificacion_usuario, codigo_producto, cantidad=1):
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            return False, "El usuario seleccionado no existe."

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            return False, "El producto seleccionado no existe."

        try:
            cantidad = int(cantidad)
        except ValueError:
            return False, "La cantidad debe ser un número entero."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor que cero."

        # La venta se registra sin implementar inventario avanzado.
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = Venta(identificacion_usuario, codigo_producto, cantidad, fecha)
        self.ventas.append(venta)
        ArchivoServicio.guardar_json(
            "ventas.json", [venta.to_dict() for venta in self.ventas]
        )
        return True, "Venta registrada correctamente."
