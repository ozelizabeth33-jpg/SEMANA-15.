class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def actualizar_stock(self, cantidad):
        self.stock += cantidad

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }

    def __str__(self):
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock}"
