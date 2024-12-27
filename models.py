from sqlalchemy import Column, Integer, String
import db


class Productos(db.Base):
    __tablename__ = "productos"
    __table_args__ = {"sqlite_autoincrement" : True}
    id_producto = Column(Integer, primary_key = True)
    nombre = Column(String, nullable = False)
    precio = Column(Integer, nullable = False)
    stock = Column(Integer, nullable = True, default = 0)
    categoria = Column(String, nullable = True, default = None)

    def __init__(self, nombre, precio, stock, categoria):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    def __str__(self):
        return (f"El producto: {self.nombre} tiene un precio de: "
                f"{self.precio} euros. Tenemos en stock {self.stock} unidades")