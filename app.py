from tkinter import ttk
from tkinter import *
import sqlite3
import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Productos


class VentanaPrincipal():
    def __init__(self, root):
        self.db_url = "sqlite:///database/productos.db"
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1) # cambiar tamaño ventana
        self.ventana.wm_iconbitmap("recursos/cardano_ada_crypto_icon_264359.ico")

        # Creación del contenedor principal (frame)
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Arial', 16, 'bold'), bg='#FF66B2',
                           fg='white')
        frame.grid(row=0, column=0, pady=20, columnspan=3, sticky="nsew")

        # Label de Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Arial', 13), bg='#FF66B2', fg='white')
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombre = Entry(frame, font=('Arial', 12))
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()

        # Label de Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Arial', 13), bg='#FF66B2', fg='white')
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame, font=('Arial', 12))
        self.precio.grid(row=2, column=1)

        # Label de Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Arial', 13), bg='#FF66B2', fg='white')
        self.etiqueta_categoria.grid(row=3, column=0)
        # Entry Categoría
        self.categoria = Entry(frame, font=('Arial', 12))
        self.categoria.grid(row=3, column=1)

        # Label de Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Arial', 13), bg='#FF66B2', fg='white')
        self.etiqueta_stock.grid(row=4, column=0)
        # Entry Stock
        self.stock = Entry(frame, font=('Arial', 12))
        self.stock.grid(row=4, column=1)

        # Botón Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 14, 'bold'), background='#FF1493', foreground='black', padding=10)
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red", bg='#FF66B2', font=('Arial', 12))
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 11), background="#F0F0F0",
                        foreground="#333333")
        style.configure("mystyle.Treeview.Heading", font=('Arial', 13, 'bold'), background='#00BFFF',
                        foreground='black')
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabla = ttk.Treeview(height=10, columns=("Nombre", "Precio", "Stock", "Categoría"),
                                  style="mystyle.Treeview")
        self.tabla.grid(row=7, column=0, columnspan=2, pady=20)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)
        self.tabla.heading('#2', text='Stock', anchor=CENTER)
        self.tabla.heading('#3', text='Categoría', anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 14, 'bold'), background='#FF1493', foreground='black', padding=10)
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=8, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.editar_producto, style='my.TButton')
        self.boton_editar.grid(row=8, column=1, sticky=W + E)

        # Crear el canvas para el gráfico de barras
        self.canvas = Canvas(self.ventana, width=500, height=300, bg='white')
        self.canvas.grid(row=10, column=0, columnspan=2, pady=20)

        # Título del gráfico
        self.titulo_grafico = Label(self.ventana, text="Gráfico de Stock de Productos", font=('Arial', 16, 'bold'),
                                    bg='#FF66B2', fg='black')
        self.titulo_grafico.grid(row=9, column=0, columnspan=2, pady=10)

        # Llamada para obtener los productos
        self.get_productos()

    def obtener_productos(self):
        session = self.Session()
        try:
            productos = session.query(Productos).all()
        except Exception as e:
            print("Hubo un error al obtener los productos de la base de datos")
            print(f"Error: {e}")
        finally:
            session.close()
        return productos


    def get_productos(self):
        # Limpiar la tabla de productos antes de mostrar los nuevos
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)


        productos = self.obtener_productos()

        # Insertar los productos en la tabla
        for producto in productos:
            self.tabla.insert("", "end", text=producto.nombre,
                              values=(producto.precio, producto.stock, producto.categoria))

        # Actualizar el gráfico después de obtener los productos
        self.mostrar_grafico()

    def mostrar_grafico(self):
        # Limpiar el canvas antes de dibujar el nuevo gráfico
        self.canvas.delete("all")

        # Obtener los productos y su stock
        productos = self.obtener_productos()

        # Verificar si hay productos antes de continuar
        if not productos:
            print("No hay productos disponibles para mostrar en el gráfico.")
            return

        # Configuración de las barras
        max_height = 200  # Altura máxima de las barras
        max_stock = max([producto.stock for producto in productos])  # Máximo stock para normalizar las barras
        bar_width = 40
        gap = 20
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#8E44AD"]
        # Dibujar las barras
        for i, producto in enumerate(productos):
            stock = producto.stock
            bar_height = (stock / max_stock) * max_height  # Normalizar la altura de la barra
            x1 = i * (bar_width + gap) + 50  # Posición en el eje X
            y1 = 250 - bar_height  # Posición en el eje Y (invirtiendo para que la barra crezca hacia arriba)
            x2 = x1 + bar_width  # Ancho de la barra
            y2 = 250  # Altura de la barra (el suelo)
            color = colors[i % len(colors)]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)  # Dibujar la barra
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=producto.nombre, anchor="center",
                                    font=('Arial', 10))
            self.canvas.create_text(x1 + bar_width / 2, y2 + 10, text=str(stock), anchor="center", font=('Arial', 10))

    def validation_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        # Validaciones
        if not self.validation_nombre():
            self.mensaje["text"] = "El nombre es obligatorio y no puede estar vacío"
            return

        if not self.validacion_precio():
            self.mensaje["text"] = "El precio es obligatorio y debe de tener un número mayor que 0"
            return

        session = self.Session()
        try:
            nuevo_producto = Productos(
                nombre=self.nombre.get(),
                precio=float(self.precio.get()),
                stock=int(self.stock.get()),
                categoria=self.categoria.get()
            )
            session.add(nuevo_producto)
            session.commit()

            self.mensaje["text"] = f"Producto {self.nombre.get()} añadido con éxito"

            # Limpiar los campos
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)

            self.get_productos()

        except Exception as e:
            session.rollback()
            self.mensaje["text"] = f"Hubo un error al añadir el producto: {str(e)}"
        finally:
            session.close()

    def del_producto(self):
        self.mensaje["text"] = ""
        try:
            nombre = self.tabla.item(self.tabla.selection())["text"]
        except IndexError:
            self.mensaje["text"] = "Por favor selecciona un producto"
            return

        session = self.Session()
        try:
            producto = session.query(Productos).filter_by(nombre=nombre).first()
            if producto:
                session.delete(producto)
                session.commit()  # Confirmar los cambios
                self.mensaje["text"] = f"Producto {nombre} eliminado con éxito"
            else:
                self.mensaje["text"] = f"Producto {nombre} no encontrado"
        except Exception as e:
            session.rollback()
            self.mensaje["text"] = f"Hubo un error al eliminar el producto: {str(e)}"
        finally:
            session.close()
        self.get_productos()

    def editar_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())["text"]
            precio = self.tabla.item(self.tabla.selection())["values"][0]
            stock = self.tabla.item(self.tabla.selection())["values"][1]
            categoria = self.tabla.item(self.tabla.selection())["values"][2]
            VentanaEditarProducto(self, nombre, precio, self.mensaje, stock, categoria)
        except IndexError:
            self.mensaje["text"] = "Por favor, seleccione un producto"


class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, stock, categoria, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.mensaje = mensaje
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", bg='#FF66B2')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", bg='#FF66B2', font=('Calibri', 16, 'bold')).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly',
              font=('Calibri', 13)).grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", bg='#FF66B2', font=('Calibri', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly',
              font=('Calibri', 13)).grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Stock antiguo (solo lectura)
        Label(frame_ep, text="Stock antiguo: ", bg='#FF66B2', font=('Calibri', 13)).grid(row=5, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=stock), state='readonly',
              font=('Calibri', 13)).grid(row=5, column=1)

        # Stock nuevo
        Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13)).grid(row=6, column=0)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=6, column=1)

        # Categoría antigua (solo lectura)
        Label(frame_ep, text="Categoría antigua: ", bg='#FF66B2', font=('Calibri', 13)).grid(row=7, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria), state='readonly',
              font=('Calibri', 13)).grid(row=7, column=1)

        # Categoría nueva
        Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13)).grid(row=8, column=0)
        self.input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=8, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))
        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=9,
                                                                                                           columnspan=2,
                                                                                                           sticky=W + E)

    def actualizar(self):
        # Obtener los nuevos valores de los campos, o mantener los actuales si están vacíos
        nuevo_nombre = self.input_nombre_nuevo.get().strip() or self.nombre
        nuevo_precio = float(self.input_precio_nuevo.get()) if self.input_precio_nuevo.get() else float(self.precio)
        if self.input_stock_nuevo.get().strip():
            nuevo_stock = int(self.input_stock_nuevo.get())
        else:
            nuevo_stock = int(self.stock.cget("text")) if self.stock.cget("text").strip() else 0
        nueva_categoria = self.input_categoria_nueva.get().strip() or self.categoria

        # Verificar que el precio y el stock son valores válidos
        try:
            # Convertir precio y stock si no están vacíos
            if self.input_precio_nuevo.get() and not self.input_precio_nuevo.get().replace('.', '', 1).isdigit():
                raise ValueError("El precio debe ser un número válido.")

            if self.input_stock_nuevo.get() and not self.input_stock_nuevo.get().isdigit():
                raise ValueError("El stock debe ser un número válido.")
        except ValueError as e:
            self.mensaje["text"] = str(e)  # Mostrar mensaje de error
            return

        # Crear sesión para actualizar el producto
        session = self.ventana_principal.Session()
        try:
            # Buscar el producto en la base de datos
            producto = session.query(Productos).filter_by(nombre=self.nombre).first()
            if producto:
                # Actualizar los valores del producto
                producto.nombre = nuevo_nombre
                producto.precio = nuevo_precio
                producto.stock = nuevo_stock
                producto.categoria = nueva_categoria
                session.commit()  # Confirmar los cambios

                # Actualizar la interfaz con un mensaje de éxito
                self.mensaje["text"] = f"Producto {nuevo_nombre} actualizado con éxito."

                # Actualizar la tabla de productos y el gráfico
                self.ventana_principal.get_productos()
                self.ventana_principal.mostrar_grafico()

                # Cerrar la ventana de edición
                self.ventana_editar.destroy()
            else:
                # Si no se encuentra el producto en la base de datos
                self.mensaje["text"] = f"Producto {self.nombre} no encontrado para actualizar."
        except Exception as e:
            # Si ocurre un error durante la actualización
            session.rollback()
            self.mensaje["text"] = f"Error al actualizar el producto: {str(e)}"
        finally:
            session.close()  # Cerrar la sesión


if __name__ == "__main__":
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
