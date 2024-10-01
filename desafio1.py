#Desafío 1
#Objetivo: Desarrollar un sistema para manejar productos en un inventario.

'''
Requisitos:

1- Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.

2- Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.

3- Implementar operaciones CRUD para gestionar productos del inventario.

4- Manejar errores con bloques try-except para validar entradas y gestionar excepciones.

5- Persistir los datos en archivo JSON.

'''
import mysql.connector
from mysql.connector import Error
from decouple import config
import json

class Producto:
    def __init__(self, codigo, nombre, marca, precio, cantidad):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__marca = marca
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def marca(self):
        return self.__marca.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    def validar_precio(self, precio):
        try:
            precio_numero = float(precio)
            if precio_numero <= 0:
                raise ValueError("El precio debe ser un número positivo")
            return precio_numero
        except ValueError:
            raise ValueError("El precio debe ser un número válido")

    
    @cantidad.setter
    def precio(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)

    def validar_cantidad(self, cantidad):
        try:
            cantidad_numero = int(cantidad)
            if cantidad_numero <= 0:
                raise ValueError("La cantidad debe ser cero o un número positivo")
            return cantidad_numero
        except ValueError:
            raise ValueError("La cantidad debe ser un número válido")



    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "marca": self.marca,
            "precio": self.precio,
            "cantidad": self.cantidad
        }
    
    def __str__(self):
        return f"{self.nombre} {self.marca}"


class ProductoAlimento(Producto):
    def __init__(self, codigo, nombre, marca, precio, cantidad, vencimiento):
        super().__init__(codigo, nombre, marca, precio, cantidad)
        self.__vencimiento = vencimiento

    @property
    def vencimiento(self):
        return self.__vencimiento
    
    def to_dict(self):
        data = super().to_dict()
        data['vencimiento'] = self.vencimiento
        return data 
    
    def __str__(self):
        return f"{super().__str__()} - vencimiento: {self.vencimiento}"
    

class ProductoElectronico(Producto):
    def __init__(self, codigo, nombre, marca, precio, cantidad, garantia):
        super().__init__(codigo, nombre, marca, precio, cantidad)
        self.__garantia = garantia
    
    @property
    def garantia(self):
        return self.__garantia
    
    def to_dict(self):
        data = super().to_dict()
        data['garantia'] = self.garantia
        return data
    
    def __str__(self):
        return f"{super().__str__()} - garantia: {self.garantia}"
    

class GestionProducto:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port= config('DB_PORT')
    
    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try: 
            connection = mysql.connector.connect(
                host= self.host,
                database= self.database,
                user= self.user,
                password= self.password,
                port= self.port
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos
               

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #verificar si el codigo existe
                    cursor.execute('SELECT codigo FROM Producto WHERE codigo = %s', (producto.codigo,))
                    if cursor.fetchone():
                        print(f'Error: ya existe un producto con el código {producto.codigo}')
                        return 
                    #insertar producto dependiendo del tipo
                    if isinstance(producto, ProductoAlimento):
                        query = '''
                        INSERT INTO producto (codigo, nombre, marca, precio, cantidad)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.marca, producto.precio, producto.cantidad))

                        query = '''
                        INSERT INTO ProductoAlimento (codigo, vencimiento)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (producto.codigo, producto.vencimiento))

                    elif isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO producto (codigo, nombre, marca, precio, cantidad)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.marca, producto.precio, producto.cantidad))

                        query = '''
                        INSERT INTO ProductoElectronico (codigo, garantia)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (producto.codigo, producto.garantia))

                    connection.commit()
                    print(f'Producto {producto.nombre} {producto.marca} creado correctamente')

        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM Producto WHERE codigo = %s', (codigo,))
                    producto_data = cursor.fetchone()

                    if producto_data:
                        cursor.execute('SELECT vencimiento FROM ProductoAlimento WHERE codigo = %s', (codigo,))
                        vencimiento = cursor.fetchone()

                        if vencimiento:
                            producto_data['vencimiento'] = vencimiento['vencimiento']
                            producto = ProductoAlimento(**producto_data)
                        else: 
                            cursor.execute('SELECT garantia FROM ProductoElectronico WHERE codigo = %s', (codigo,))
                            garantia = cursor.fetchone()
                            if garantia:
                                producto_data['garantia'] = garantia['garantia']
                                producto = ProductoElectronico(**producto_data)
                            else:
                                producto = Producto(**producto_data)
                        
                        print(f'Producto encontrado: {producto}')
                    
                    else: 
                        print(f'No se encontró producto con codigo {codigo}.')
        
        except Error as e:
            print(f'Error al leer producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_cantidad_producto(self, codigo, nueva_cantidad):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #verificación del código
                    cursor.execute('SELECT * FROM Producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print(f'No existe el producto con el código: {codigo}.')
                        return

                    #actualizar cantidad del producto
                    cursor.execute('UPDATE producto SET cantidad = %s WHERE codigo = %s', (nueva_cantidad, codigo))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'La cantidad ha sido actualizada para el producto con el código: {codigo}')
                    else:
                        print(f'No se encontró el producto con el código: {codigo}')

        except Exception as e:
            print(f'Error al actualizar el producto:{e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self, codigo):
        try:
            connection = self.connect()
            if connection: 
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM Producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print(f'No existe el producto con el código: {codigo}.')
                        return
                    
                    #Eliminar producto
                    cursor.execute('DELETE FROM ProductoAlimento WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM ProductoElectronico WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM Producto WHERE codigo = %s', (codigo,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Producto con código {codigo} eliminado exitosamente')
                    else:
                        print(f'No existe el producto con el código: {codigo}')

        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()


    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data = cursor.fetchall()

                    productos = []
                    for producto_data in productos_data:
                        codigo = producto_data['codigo']

                        cursor.execute('SELECT vencimiento FROM ProductoAlimento WHERE codigo = %s', (codigo,))
                        vencimiento = cursor.fetchone()

                        if vencimiento:
                            producto_data['vencimiento'] = vencimiento['vencimiento']
                            producto = ProductoAlimento(**producto_data)
                        else:
                            cursor.execute('SELECT garantia FROM ProductoElectronico WHERE codigo = %s', (codigo,))
                            garantia = cursor.fetchone()
                            producto_data['garantia'] = garantia['garantia']
                            producto = ProductoElectronico(**producto_data)

                        productos.append(producto)

        except Error as e:
            print(f'Error al mostrar los productos: {e}')
        else:
            return productos
        finally:
            if connection.is_connected():
                connection.close()      