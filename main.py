import os
import platform

from desafio1 import (
    ProductoAlimento,
    ProductoElectronico,
    GestionProducto,
)

def limpiar_pantalla():
    '''Limpiar la pantalla según el sistema operativo '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # P/ Linux-Unix-Mac

def mostrar_menu():
    print(">>>>>> Menú de gestión de productos <<<<<<<")
    print("1. Agregar producto alimento")
    print("2. Agregar producto electrónico")
    print("3. Buscar producto por codigo")
    print("4. Actualizar cantidad")
    print("5. Eliminar producto por codigo")
    print("6. Mostrar todos los productos")
    print("7. Salir")
    print("=========================================")


def agregar_producto(gestion, tipo_producto):
    try:
        codigo = int(input('Ingrese el código del producto: '))
        nombre = input('Ingrese nombre del producto: ')
        marca = input('Ingrese marca del producto: ')
        precio = float(input('Ingrese precio del producto: '))
        cantidad = int(input('Ingrese cantidad del producto: '))

        if tipo_producto == '1':
            vencimiento= int(input('Ingrese vencimiento (meses) del producto:'))
            producto = ProductoAlimento(codigo, nombre, marca, precio, cantidad, vencimiento)
        elif tipo_producto == '2':
            garantia = int(input('Ingrese meses de garantía (meses) del producto:'))
            producto = ProductoElectronico(codigo, nombre, marca, precio, cantidad, garantia)
        else: 
            print('Opción no válida')
            return


        gestion.crear_producto(producto)
        input('Presione enter para continuar')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e: 
        print(f'Error inesperado: {e}')

def buscar_producto_por_codigo(gestion):
    codigo = input('Ingrese el codigo del producto a buscar: ')
    gestion.leer_producto(codigo)
    input('Presione enter para continuar...')

def actualizar_cantidad_producto(gestion):
    codigo = input('Ingrese el codigo del producto para actualizar cantidad del producto en stock: ')
    cantidad = int(input('Ingrese la cantidad del producto: '))
    gestion.actualizar_cantidad_producto(codigo, cantidad)
    input('Presione enter para continuar...')

def eliminar_producto_por_codigo(gestion):
    codigo = input('Ingrese el codigo del producto a eliminar: ')
    gestion.eliminar_producto(codigo)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    print('=========== Listado completo de los productos =============')
    try:
        productos = gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto, ProductoAlimento):
                print(f'{producto.codigo} {producto.nombre} {producto.vencimiento}')
            elif isinstance(producto, ProductoElectronico):
                print(f'{producto.codigo} {producto.nombre} {producto.garantia}')
    
    except Exception as e:
        print(f'Error al mostrar los productos {e}')



    for producto in gestion.leer_datos().values():
        if 'vencimiento' in producto:
            print(f"{producto['nombre']} - {producto['marca']} - Vencimiento {producto['vencimiento']} meses")
        else:
            print(f"{producto['nombre']} - {producto['marca']} - Garantia {producto['garantia']} meses")
    print('=======================================================')
    input('Presione enter para continuar...')


if __name__ == "__main__":
    gestion = GestionProducto()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2': 
            agregar_producto(gestion, opcion)

        elif opcion == '3':
            buscar_producto_por_codigo(gestion)

        elif opcion == '4':
            actualizar_cantidad_producto(gestion)

        elif opcion == '5':
            eliminar_producto_por_codigo(gestion)

        elif opcion == '6':
            mostrar_todos_los_productos(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        
        else:
            print('Opción no válida. Por favor selecciones una opcion valida (1-7)')