from tkinter import ttk
from tkinter import *
import sqlite3

class VentanaPrincipal():
    db = "database/productos.db"
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)  # Activa la redimension de la ventana
        self.ventana.wm_iconbitmap("recursos/cardano_ada_crypto_icon_264359.ico")

        # Creación del contenedor principal (frame)
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Arial', 16, 'bold'), bg='#FF66B2', fg='white')
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

        # Botón Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 14, 'bold'), background='#FF1493', foreground='black', padding=10)
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red", bg='#FF66B2', font=('Arial', 12))
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 11), background="#F0F0F0", foreground="#333333")
        style.configure("mystyle.Treeview.Heading", font=('Arial', 13, 'bold'), background='#00BFFF', foreground='black')  # Títulos en negro
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=2, pady=20)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 14, 'bold'), background='#FF1493', foreground='black', padding=10)
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=6, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=6, column=1, sticky=W + E)
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            self.tabla.insert("", 0, text=fila[1], values=fila[2])

        # Cambiar el color del texto en las filas de la tabla a negro
        for item in self.tabla.get_children():
            self.tabla.item(item, tags='black')
        self.tabla.tag_configure('black', foreground='black')

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

        query = "INSERT INTO producto VALUES(NULL, ?, ?)"
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        self.mensaje["text"] = "Producto {} añadido con éxito".format(self.nombre.get())
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
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
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
            self.mensaje["text"] = "Por favor, seleccione un producto"

class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar producto")
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Arial', 16, 'bold'), bg='#FF66B2', fg='white')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        Label(frame_ep, text="Nombre antiguo: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Arial', 13)).grid(row=1, column=1)
        Label(frame_ep, text="Nombre nuevo: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        Label(frame_ep, text="Precio antiguo: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Arial', 13)).grid(row=3, column=1)
        Label(frame_ep, text="Precio nuevo: ", font=('Arial', 13), bg='#FF66B2', fg='white').grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Arial', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=5,columnspan=2,sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        if nuevo_nombre and nuevo_precio:
            query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?"
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje["text"] = f"El producto {self.nombre} ha sido actualizado con éxito"
        else:
            self.mensaje["text"] = f"No se pudo actualizar el producto {self.nombre}"

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()

if __name__ == "__main__":
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
