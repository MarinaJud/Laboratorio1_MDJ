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
    def __init__(self, archivo):
        self.archivo = archivo

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
            datos = self.leer_datos()
            codigo = producto.codigo
            if not str(codigo) in datos.keys():
                datos[codigo] = producto.to_dict()
                self.guardar_datos(datos)
                print(f'Ha sido guardado correctamente')
            else:
                print(f"Ya existe el producto {codigo}.")
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if codigo in datos:
                producto_data = datos[codigo]
                if 'vencimiento' in producto_data:
                    producto = ProductoAlimento(**producto_data)
                else:
                    producto = ProductoElectronico(**producto_data)
                print(f'producto encontrado con el codigo {codigo}')
            else:
                print(f'No se encontró al producto con codigo: {codigo}')

        except Exception as e:
            print(f'Error al leer producto: {e}')

    def actualizar_cantidad_producto(self, codigo, nueva_cantidad):
        try:
            datos = self.leer_datos()
            if str(codigo) in datos.keys():
                datos[codigo]['cantidad'] = nueva_cantidad
                self.guardar_datos(datos)
                print(f'Cantidad actualizada para el producto con codigo {codigo}')
            else: 
                print(f'No se encontro el producto con codigo {codigo}')
        except Exception as e:
            print(f'Error al actualizar el producto:{e}')

    def eliminar_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if str(codigo) in datos.keys():
                del datos[codigo]
                self.guardar_datos(datos)
                print(f'El producto con codigo {codigo} ha sido eliminado')
            else: 
                print(f'No se encontro el producto con codigo {codigo}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')

        