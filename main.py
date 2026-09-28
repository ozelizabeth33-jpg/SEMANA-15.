import tkinter as tk

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


def abrir_aplicacion_principal():
    ventana = tk.Tk()
    servicio = RestauranteServicio()

    def cerrar_sesion():
        ventana.destroy()
        iniciar()

    MainView(ventana, servicio, cerrar_sesion)
    ventana.mainloop()


def iniciar():
    servicio = RestauranteServicio()
    ventana_login = tk.Tk()
    LoginView(ventana_login, servicio, abrir_aplicacion_principal)
    ventana_login.mainloop()


if __name__ == "__main__":
    iniciar()
