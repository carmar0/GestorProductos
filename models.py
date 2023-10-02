import sqlite3
import tkinter
from tkinter import *
from tkinter import ttk

class Producto:

    db = "database/productos.db"  # ruta de la base de datos

    def __init__(self, root):  # vinculamos la clase Producto con la interfaz gráfica de tkinter a través de la ventana principal root
        self.ventana = root  # llamamos ventana a la variable que controla la ventana principal/root de la aplicación

        # personalizamos la ventana:
        self.ventana.title("App Gestor de Productos") # Título de la ventana
        self.ventana.resizable(1,1)  # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico") # cambiamos el icono (esquina superior izquierda de la ventana principal)
        self.ventana.configure(bg='LightCyan2')  # color del background

        # Creación del contenedor Frame principal (en la ventana principal)
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold')) #contenedor de widgets que dibuja un borde en torno a su tamaño
        frame.grid(row=0, column=0, columnspan=4, pady=20)  # ubicación del contendor Frame
                                                            # columnspan=4 -> frame de 4 columnas
                                                           # pady establece el margen con el borde superior de la ventana

        # Ahora creamos los distintos widgets dentro del Frame principal
        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre.grid(row=1, column=0)   # Posicionamiento de la esquina superior izquierda del frame a través de grid
        # Entry Nombre (caja de texto que recibirá el nombre)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()  # Para que el foco del ratón vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=2, column=0)
        # Menu de selección de Categoría
        s = ttk.Style()
        s.configure('TMenubutton', font=('Calibri', 13))
        opciones = ["Seleccione una opción", "Ropa", "Calzado", "Producto del hogar", "Electrodoméstico", "Mueble", "Aparato electrónico", "Otro"]
        self.opcion_seleccionada = StringVar()  # variable de tipo string que almacenará la opción seleccionada del menú desplegable
        self.categoria = ttk.OptionMenu(frame, self.opcion_seleccionada, *opciones, style='TMenubutton')
        self.categoria.grid(row=2, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=3, column=0)
        # Entry Precio (caja de texto que recibirá el precio)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=3, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiqueta_stock.grid(row=4, column=0)
        # Entry Stock (caja de texto que recibirá el stock)
        self.stock = Entry(frame, font=('Calibri', 13))
        self.stock.grid(row=4, column=1)

        # Botón de Guardar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
                                                        #usamos el boton de la libreria ttk
                                                     # en command se pone la función (sin paréntesis) que se desea ejecutar al pulsar el botón
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W+E) # columnspan=2 para que sea de 2 columnas y
                                             # con el atributo sticky se le dice cuanto se quiere que ocupe. En este
                                             # caso se le dice que ocupe todo el ancho, desde el oeste (W) hasta el este (E)
        self.mensaje = Label(text="", fg="red", background='LightCyan2', font=('Calibri', 13))  # text vacío para poder añadirlo después
        self.mensaje.grid(row=6, column=0, columnspan=4, sticky=W+E)

        # Tabla de Productos (no está dentro del frame anterior)
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11), background='azure')  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])  # Eliminamos los bordes
        # Estructura de la tabla (widget Treeview de la sub librería ttk)
        self.tabla = ttk.Treeview(height=20, columns=('#1','#2','#3','#4'), show="headings", style="mystyle.Treeview")  # altura de 20 filas
        self.tabla.grid(row=7, column=0, columnspan=4)  # posicionamiento de la esquina superior izquierda de la tabla. Ancho de 4 columnas
        # gracias al parámetro show="headings" de Treeview podemos añadir los headings a las columnas de la siguiente manera:
        self.tabla.heading("#1", text="Nombre", anchor=CENTER)
        self.tabla.heading("#2", text="Categoría", anchor=CENTER)
        self.tabla.heading("#3", text="Precio [€]", anchor=CENTER)
        self.tabla.heading("#4", text="Stock", anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text='ELIMINAR',  style="my.TButton", command=self.del_producto) #al pulsarlo se ejecuta del_producto()
        boton_eliminar.grid(row=8, column=0, columnspan=2, sticky=W+E)
        boton_editar = ttk.Button(text='EDITAR',  style="my.TButton", command=self.edit_producto) # al pulsarlo se ejecuta edit_producto()
        boton_editar.grid(row=8, column=2, columnspan=2, sticky=W+E)

        self.get_productos()



    # método que se conecta a la base de datos, ejecuta una consulta y cierra la conexión.
    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con: # Iniciamos una conexión con la base de datos (alias con)
            cursor = con.cursor()        # Generamos un cursor de la conexión para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros) # Preparar la consulta SQL (con parametros si los hay)
            con.commit()                # Ejecutar la consulta SQL preparada anteriormente
        return resultado                # Retornar el resultado de la consulta SQL


    # método que devuelva un listado de todos los productos de la base de datos
    def get_productos(self):

        registros_tabla = self.tabla.get_children() # obtenemos los productos que hay en la tabla
        for fila in registros_tabla:               # y los eliminamos. Vaciamos la tabla
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)      # consultamos los productos que hay en la base de datos
        #print(registros)

        for fila in registros:         # actualizamos la tabla de productos
            print(fila)
            self.tabla.insert("", 0, text = fila[1] , values = fila[1:]) # en la primera columna se inserta el nombre
                                                            # y a continuación se insertan las siguientes columnas

    # método para validar que se ha introducido un nombre
    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    # método para validar que se ha introducido un precio
    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    # método para validar que se ha seleccionado una categoría
    def validacion_categoria(self):
        return self.opcion_seleccionada.get() != "Seleccione una opción"

    # método para validar que se ha introducido un stock
    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0

    # método para añadir un nuevo producto
    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = "INSERT INTO producto VALUES(NULL,?,?,?,?)"  # el id es AUTOINCREMENTAL --> necesario poner NULL
            parametros = (self.nombre.get(), self.opcion_seleccionada.get(), self.precio.get(), self.stock.get())  # IMPORTANTE que sea una tupla
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.opcion_seleccionada.set("Seleccione una opción")  # Reiniciar el campo categoría del formulario
            self.stock.delete(0, END)  # Borrar el campo stock del formulario

            #Para debug
            #print(self.nombre.get())
            #print(self.precio.get())

        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_stock():
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_stock():
            print("Seleccione una categoría")
            self.mensaje["text"] = "Seleccione una categoría"
        else:   # si olvidamos de introducir más de un dato
            print("Todos los campos son obligatorios")
            self.mensaje["text"] = "Todos los campos son obligatorios"

        self.get_productos()  #  Cuando se finalice la insercion de datos actualizamos la tabla de productos en la aplicación
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio

    # método para eliminar un producto
    def del_producto(self):
        # Debug
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())['text'])
        #print(self.tabla.item(self.tabla.selection())['values'])
        #print(self.tabla.item(self.tabla.selection())['values'][0])
        #print(self.tabla.item(self.tabla.selection()))

        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se selecciona un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]  # el selection() corresponde a donde clicamos
                                                                # el item() corrersponde a su registro completo
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))  # se elimina de la base de datos. (nombre,) -> la coma es necesaria para indicar que es una tupla
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()                # se actualiza la tabla de productos en la aplicación

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        #print(self.tabla.item(self.tabla.selection()))  # devuelve un diccionario con clave texto y valor el resto de columnas
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_categoria = self.tabla.item(self.tabla.selection())['values'][1] # La categoria, precio y stock se encuentran dentro de una lista
        old_precio = self.tabla.item(self.tabla.selection())['values'][2]
        old_stock = self.tabla.item(self.tabla.selection())['values'][3]

        # ventana nueva (editar producto)
        self.ventana_editar = Toplevel() # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto" # Titulo de la ventana
        self.ventana_editar.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico') # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 30, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold')) # frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text = "Nombre antiguo: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_antiguo.grid(row=2, column=0) # Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus() # Para que el foco del raton vaya a este Entry al inicio

        # Label Categoría antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoría antigua: ", font=('Calibri', 13)) # Etiqueta de categoría ubicada en el frame
        self.etiqueta_categoria_antigua.grid(row=4, column=0) # Posicionamiento a traves de grid
        # Entry Categoría antigua (texto que no se podra modificar)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria), state='readonly', font=('Calibri', 13))
        self.input_categoria_antigua.grid(row=4, column=1)

        # Label Categoría nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=5, column=0)
        # Menu de selección de Categoría nueva
        s = ttk.Style()
        s.configure('TMenubutton', font=('Calibri', 13))
        opciones = ["Seleccione una opción", "Ropa", "Calzado", "Producto del hogar", "Electrodoméstico", "Mueble", "Aparato electrónico", "Otro"]
        self.input_opcion_seleccionada = StringVar()  # variable de tipo string que almacenará la opción seleccionada del menú desplegable
        self.input_categoria_nueva = ttk.OptionMenu(frame_ep, self.input_opcion_seleccionada, *opciones, style='TMenubutton')
        self.input_categoria_nueva.grid(row=5, column=1)

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=6, column=0) # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=6, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=7, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_antiguo.grid(row=8, column=0) # Posicionamiento a traves de grid
        # Entry Stock antiguo (texto que no se podra modificar)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), state='readonly', font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry Stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=lambda:
                                       self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                 self.input_nombre_antiguo.get(),
                                                                 self.input_opcion_seleccionada.get(),
                                                                 self.input_categoria_antigua.get(),
                                                                 self.input_precio_nuevo.get(),
                                                                 self.input_precio_antiguo.get(),
                                                                 self.input_stock_nuevo.get(),
                                                                 self.input_stock_antiguo.get()))
                                    # al pulsar ese boton se ejecuta el método actualizar_productos()
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)


    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nueva_categoria, antigua_categoria, nuevo_precio, antiguo_precio,
                             nuevo_stock, antiguo_stock):

        producto_modificado = False
        query = 'UPDATE producto SET nombre=?, categoria=?, precio=?, stock=? WHERE nombre=? AND categoria=? AND precio=? AND stock=?'

        if nuevo_nombre == '':                                      # si no se inserta un nombre nuevo
            nombre_actualizado = self.input_nombre_antiguo.get()   # se mantiene el antiguo
        else:
            nombre_actualizado = self.input_nombre_nuevo.get()
            producto_modificado = True

        if nueva_categoria == "Seleccione una opción":                 # si no se selecciona una nueva categoría
            categoria_actualizada = self.input_categoria_antigua.get()  # se mantiene la aantigua
        else:
            categoria_actualizada = self.input_opcion_seleccionada.get()
            producto_modificado = True

        if nuevo_precio == '':                                     # si no se inserta un precio nuevo
            precio_actualizado = self.input_precio_antiguo.get()   # se mantiene el antiguo precio
        else:
            precio_actualizado = self.input_precio_nuevo.get()
            producto_modificado = True

        if nuevo_stock == '':                                     # si no se inserta un stock nuevo
            stock_actualizado = self.input_stock_antiguo.get()      # se mantiene el antiguo stock
        else:
            stock_actualizado = self.input_stock_nuevo.get()
            producto_modificado = True

        parametros = (nombre_actualizado, categoria_actualizada, precio_actualizado, stock_actualizado, antiguo_nombre, antigua_categoria,
                      antiguo_precio, antiguo_stock)

        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario
