class Venta:
    def __init__(self, identificacion_usuario, codigo_producto, cantidad=1, fecha=""):
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.cantidad = int(cantidad)
        self.fecha = fecha

    def to_dict(self):
        return {
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
        }

    def __str__(self):
        return (
            f"Usuario: {self.identificacion_usuario} | "
            f"Producto: {self.codigo_producto} | "
            f"Cantidad: {self.cantidad} | Fecha: {self.fecha}"
        )
