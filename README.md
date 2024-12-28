# Gestor de Productos - Aplicación de Escritorio

Este es un proyecto de gestión de productos utilizando **Python**, **Tkinter** para la interfaz de usuario,
**SQLite** como base de datos y **SQLAlchemy** como ORM para la gestión de la base de datos. La aplicación permite gestionar
productos de forma sencilla y visualizar un gráfico con los stocks disponibles de los productos.

## Características

- **Añadir productos**: Los usuarios pueden añadir nuevos productos con información como nombre, categoría, precio y cantidad.
- **Ver productos**: Visualización de todos los productos almacenados en la base de datos.
- **Actualizar productos**: Los usuarios pueden actualizar la información de los productos existentes.
- **Eliminar productos**: Los usuarios pueden eliminar productos de la base de datos.
- **Gráfico de stocks**: Muestra un gráfico visual de los stocks disponibles de los productos.
- **Base de datos SQLite**: Utiliza una base de datos ligera y fácil de usar.
- **Interfaz de usuario con Tkinter**: Interfaz gráfica sencilla para interactuar con la aplicación.

## Requisitos

- **Python 3.x**
- **Tkinter**: Para crear la interfaz gráfica de usuario.
- **SQLite**: Base de datos integrada en Python.
- **SQLAlchemy**: ORM utilizado para la gestión de la base de datos.

## Instalación

1. **Clonar el repositorio**:

   git clone https://github.com/tu_usuario/gestor-de-productos.git

   Crear un entorno virtual (opcional, pero recomendado):
Copiar código
python -m venv venv

Activar el entorno virtual:
En Windows:
Copiar código
.\venv\Scripts\activate
En Mac/Linux:
Copiar código
source venv/bin/activate

Instalar las dependencias:
Copiar código
pip install -r requirements.txt

Configurar la base de datos:
Asegúrate de tener una base de datos SQLite configurada. Si usas SQLAlchemy, puedes inicializar la base de datos con el
siguiente comando:
python app.py



Uso

Añadir un producto:
El formulario de la parte de arriba de la pagina sirve para añadir productos a la Base de Datos

Ver productos:
En la ventana principal podrás ver una lista de todos los productos almacenados en la base de datos.

Actualizar un producto:
Selecciona un producto de la lista, edítalo y guarda los cambios.

Eliminar un producto:
Selecciona un producto de la lista y haz clic en "Eliminar".

Gráfico de stocks:
La aplicación muestra un gráfico visual de los stocks disponibles de todos los productos en el sistema. 
Este gráfico se actualiza automáticamente con los cambios en los productos.
