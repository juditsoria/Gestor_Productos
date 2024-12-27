from tkinter import ttk
from tkinter import *
import sqlite3


class VentanaPrincipal():
    db = "database/productos.db"

    def __init__(self, root):
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
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=8, column=1, sticky=W + E)

        # Crear el canvas para el gráfico de barras
        self.canvas = Canvas(self.ventana, width=500, height=300, bg='white')
        self.canvas.grid(row=10, column=0, columnspan=2, pady=20)

        # Título del gráfico
        self.titulo_grafico = Label(self.ventana, text="Gráfico de Stock de Productos", font=('Arial', 16, 'bold'),
                                    bg='#FF66B2', fg='black')
        self.titulo_grafico.grid(row=9, column=0, columnspan=2, pady=10)

        # Llamada para obtener los productos después de la inicialización
        self.get_productos()

    def obtener_productos(self):
        # Consulta para obtener los nombres de los productos y su stock
        query = "SELECT nombre, stock FROM producto"
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute(query)
            productos = cursor.fetchall()  # Devuelve una lista de tuplas (nombre, stock)
        return productos

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        # Limpiar la tabla de productos antes de mostrar los nuevos
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            self.tabla.insert("", "end", text=fila[1], values=(fila[2], fila[3], fila[4]))

        # Actualizar el gráfico después de obtener los productos
        self.mostrar_grafico()

    def mostrar_grafico(self):
        # Limpiar el canvas antes de dibujar el nuevo gráfico
        self.canvas.delete("all")

        # Obtener los productos y su stock
        productos = self.obtener_productos()

        # Configuración de las barras
        max_height = 200  # Altura máxima de las barras
        max_stock = max([producto[1] for producto in productos])  # Máximo stock para normalizar las barras
        bar_width = 40
        gap = 20

        # Dibujar las barras
        for i, (producto, stock) in enumerate(productos):
            bar_height = (stock / max_stock) * max_height  # Normalizar la altura de la barra
            x1 = i * (bar_width + gap) + 50  # Posición en el eje X
            y1 = 250 - bar_height  # Posición en el eje Y (invirtiendo para que la barra crezca hacia arriba)
            x2 = x1 + bar_width  # Ancho de la barra
            y2 = 250  # Altura de la barra (el suelo)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")  # Dibujar la barra
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=producto, anchor="center", font=('Arial', 10))
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
        if not self.validation_nombre():
            self.mensaje["text"] = "El nombre es obligatorio y no puede estar vacío"
            return
        if not self.validacion_precio():
            self.mensaje["text"] = "El precio es obligatorio y debe de tener un número mayor que 0"
            return

        query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"
        parametros = (self.nombre.get(), self.precio.get(), self.stock.get(), self.categoria.get())
        self.db_consulta(query, parametros)
        self.mensaje["text"] = "Producto {} añadido con éxito".format(self.nombre.get())
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        self.categoria.delete(0, END)
        self.stock.delete(0, END)
        self.get_productos()

    def del_producto(self):
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError:
            self.mensaje["text"] = "Por favor selecciona un producto"
            return

        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "Producto {} eliminado con éxito".format(nombre)
        self.get_productos()

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())["text"]
            precio = self.tabla.item(self.tabla.selection())["values"][0]
        except IndexError:
            self.mensaje["text"] = "Por favor selecciona un producto"
            return
        self.ventana_editar = Toplevel(self.ventana)
        self.ventana_editar.title("Editar producto")

        frame_ep = LabelFrame(self.ventana_editar, text="Modificar Producto", font=('Arial', 16, 'bold'), bg='#FF66B2',
                              fg='white')
        frame_ep.grid(row=0, column=0, pady=20, columnspan=3, sticky="nsew")

        self.input_nombre_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_nombre_nuevo.insert(0, nombre)
        self.input_nombre_nuevo.grid(row=3, column=1)

        Label(frame_ep, text="Precio: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly',
              font=('Arial', 13)).grid(row=3, column=1)

        Label(frame_ep, text="Precio nuevo: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        self.boton_guardar = ttk.Button(frame_ep, text="Guardar cambios", command=self.editar_producto,
                                        style="my.TButton")
        self.boton_guardar.grid(row=5, columnspan=2, pady=10, sticky=W + E)

    def editar_producto(self):
        nombre_nuevo = self.input_nombre_nuevo.get()
        precio_nuevo = self.input_precio_nuevo.get()

        query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?"
        parametros = (nombre_nuevo, precio_nuevo, self.nombre)
        self.db_consulta(query, parametros)
        self.mensaje["text"] = "Producto actualizado con éxito"

        self.get_productos()
        self.ventana_editar.destroy()


# Inicialización de la ventana principal
root = Tk()
app = VentanaPrincipal(root)
root.mainloop()
