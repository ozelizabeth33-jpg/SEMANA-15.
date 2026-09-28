# RESTAURANTE APP - SEMANA 15

## Programación Orientada a Objetos

Aplicación gráfica para la gestión básica de un restaurante, evolucionada desde la Semana 14. Esta versión conserva el inicio de sesión, usuarios y gestión de productos e incorpora el registro de ventas para demostrar los fundamentos básicos del manejo de eventos.

## Objetivo de la Semana 15

La nueva operación permite relacionar un usuario con un producto. Desde la interfaz, el usuario selecciona ambos elementos y pulsa **Registrar venta**. El botón utiliza `command=` para ejecutar un callback; el callback obtiene la información seleccionada, delega la operación a `RestauranteServicio`, y después actualiza la tabla y comunica el resultado mediante la interfaz.

Flujo implementado:

```text
Usuario
  ↓
Botón Registrar venta
  ↓
command=self.registrar_venta
  ↓
Callback registrar_venta()
  ↓
RestauranteServicio
  ↓
ventas.json
  ↓
Tabla de ventas + mensaje visual
```

## Estructura

```text
aplicacion_restaurante/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   └── venta.png
├── main.py
└── README.md
```

## Funcionalidades

- Inicio de sesión mediante identificación y nombre.
- Consulta de usuarios.
- Registro, consulta, actualización y eliminación de productos.
- Persistencia de usuarios, productos y ventas mediante JSON.
- Sección de Ventas.
- Selección de usuario mediante `ttk.Combobox`.
- Selección de producto mediante `ttk.Combobox`.
- Registro de cantidad.
- Registro automático de fecha y hora.
- Visualización de ventas en `ttk.Treeview`.
- Botón de venta asociado mediante `command=` a un callback.
- Validaciones de usuario, producto y cantidad dentro de `RestauranteServicio`.
- Logo e ícono incorporados desde la carpeta `assets/`.

## Persistencia

Las ventas se guardan en:

`datos/ventas.json`

Cada nueva venta conserva la identificación del usuario, código del producto, cantidad y fecha de registro.

## Separación de responsabilidades

- **Modelos:** representan Usuario, Producto y Venta.
- **ArchivoServicio:** realiza lectura y escritura de archivos JSON.
- **RestauranteServicio:** contiene validaciones y operaciones del sistema.
- **MainView:** coordina la interacción gráfica y los callbacks.
- **main.py:** inicia la aplicación y controla el flujo de inicio de sesión.

La interfaz no escribe directamente en los archivos JSON.

## Ejecución

Se requiere Python 3.x.

Desde una terminal ubicada dentro de `aplicacion_restaurante` ejecutar:

```bash
python main.py
```

No se requieren librerías externas para ejecutar la aplicación.

## Prueba de la venta

1. Ejecutar `main.py`.
2. Iniciar sesión con un usuario existente de `datos/usuarios.json`.
3. Entrar a **Ventas**.
4. Seleccionar un usuario.
5. Seleccionar un producto.
6. Ingresar la cantidad.
7. Pulsar **Registrar venta**.
8. Verificar el mensaje de confirmación.
9. Verificar que la venta aparezca en la tabla.
10. Revisar `datos/ventas.json`.
11. Cerrar y volver a ejecutar para comprobar la persistencia.

## Tecnologías

- Python
- Tkinter / ttk
- Programación Orientada a Objetos
- Archivos JSON
- Visual Studio Code
- GitHub
