from tkinter import ttk  # ttk tiene los componentes graficos (botones, etiquetas, columnas...)
from tkinter import *
import sqlite3
from models import Producto


if __name__ == "__main__":
    root = Tk() # Instancia de la ventana principal de la aplicación de escritorio (Tk es el constructor de tkinter)
    app = Producto(root) # Se envía a la clase Producto el control sobre la ventana root. Esa ventana se personaliza
                         # en el constructor de la clase Producto
    root.mainloop() # Comenzamos el bucle de aplicacion, es como un while True -> la instancia de esa ventana se queda abierta/viva.