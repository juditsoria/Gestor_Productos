from tkinter import ttk
from tkinter import *

class VentanaPrincipal():
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1) # Activa la redimension de la ventana
        self.ventana.wm_iconbitmap("recursos/cardano_ada_crypto_icon_264359.ico")

        # creacion del contenedor principal(frame)
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto")
        frame.grid(row=0, column=0, pady=20, columnspan=3)

        # Label de Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()

        # Label de Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Nombre
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Boton añadir producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar producto")
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W+E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',
                                                                              11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':
                                                                             'nswe'})])  # Eliminamos los bordes
        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1

if __name__ == "__main__":
    root = Tk() # constructor, instancia ventana principal
    app = VentanaPrincipal(root) # creao objeto VentanaPrincipal y le paso la ventana
    root.mainloop() # mantener la ventana abierta