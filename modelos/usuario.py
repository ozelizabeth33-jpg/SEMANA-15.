class Usuario:
    def __init__(self, identificacion, nombre):
        self.identificacion = identificacion
        self.nombre = nombre

    def __str__(self):
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre}"
