import sqlite3
from sqlite3 import Error

# Función Conexión
def conexion():
    try:
        con = sqlite3.connect("Veterinaria.db")
        return con
    except Error:
        print("No se pudo conectar con la base de datos")

# Función Creación de Tablas
def crearTabla(con):
    respuestas_válidas = ["si", "no"]
    cursor = con.cursor()
    nombreT = input("Ingrese el nombre de la Tabla a crear: ")
    Query = f"CREATE TABLE {nombreT} ( "
    executor = ""
    while executor != "no":
        Query += input("Ingrese la siguiente sentencia --> ")
        executor = input("¿Desea continuar actualizando la tabla? --> ").lower()
        while executor not in respuestas_válidas:
            print("Respuesta invalida")
            executor = input("¿Desea continuar actualizando la tabla? --> ").lower()
    try:
        cursor.execute(Query)
        con.commit()
    except Error:
        print("Cuenta con algún error en su tabla, asegúrese de haber ingresado los datos correctamente.")

# Función Impresión de Tablas
def imprimirTabla(con):
    print("Tablas Disponibles: ")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    for tabla in tablas:
        print(tabla[0])

# Función obtenimiento de Tablas
def ObtenerTablas(con):
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    return tablas

# Función obtenimiento de columnas
def columnasTablas(con, nom):
    cursor = con.cursor()
    cursor.execute(f"PRAGMA table_info({nom});")
    columnas = cursor.fetchall()
    nombres_columnas = [fila[1] for fila in columnas]
    return nombres_columnas

# Función insertar datos
def insertarTabla(con, nom):
    nombre = columnasTablas(con, nom)
    nombre = tuple(nombre)
    print(f"Insertar los siguientes datos en el orden especificado: {nombre}")
    cursor = con.cursor()
    Query = (f"INSERT INTO {nom}{nombre}Values(")
    for x in range(0, len(nombre)):
        sen = input("--> ")
        if x == len(nombre) - 1:
            Query = f'{Query}"{sen}")'
        else:
            Query = f'{Query}"{sen}",'
    print(Query)
    cursor.execute(Query)
    con.commit()

# Función modificar datos
def modificarTabla(con, nom, mod):
    cursor = con.cursor()
    cursor.execute(f"SELECT {nom} FROM {mod}")
    mods = cursor.fetchall()
    dniS = [nom[0] for nom in mods]
    print(dniS)
    nombre_columnas = columnasTablas(con, mod)
    print(f"Digite la clave a modificar: ")
    clave = input("--> ")
    while clave not in dniS:
        clave = input("--> ")
    print(f"Digite la columna a modificar: {nombre_columnas} ")
    modificador = input("--> ")
    while modificador not in nombre_columnas:
        modificador = input("--> ")
    nuevo = input("Ingresa el valor para intercambiarlo:")
    cursor.execute(f"UPDATE {mod} SET {modificador}=? WHERE {nom}=?", (nuevo, clave))
    con.commit()

# Función modificar datos
def eliminarTabla(con, nom, mod):
    cursor = con.cursor()
    cursor.execute(f"SELECT {nom} FROM {mod}")
    mods = cursor.fetchall()
    dniS = [nom[0] for nom in mods]
    print(dniS)
    print(f"Digite la clave a borrar: ")
    clave = input("--> ")
    while clave not in dniS:
        clave = input("--> ")
    cursor.execute(f"DELETE FROM {mod} WHERE {nom}=?", (clave,))
    con.commit()

# Función buscar datos
def buscarTabla(con, nom, mod):
    cursor = con.cursor()
    cursor.execute(f"SELECT {mod} FROM {nom}")
    mods = cursor.fetchall()
    dniS = [mod[0] for mod in mods]
    print(dniS)
    print(f"Digite la clave a buscar: ")
    clave = input("--> ")
    while clave not in dniS:
        clave = input("--> ")
    cursor.execute(f"SELECT * FROM {nom} WHERE {mod}=?", (clave,))
    sentencia=cursor.fetchall()
    print(sentencia)

#Función Lista DATOS
def ListaTabla(con, nom):
    columnas=columnasTablas(con,nom)
    print(columnas)
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {nom}")
    sentencia=cursor.fetchall()
    for x in sentencia:
        print(x)

# Menu de ingreso de tablas base
def menu_ingreso_base(con):
    executor = ""
    while executor != "no":
        crearTabla(con)
        executor = input("¿Desea continuar agregando Tablas?--> ")
    imprimirTabla(con)

def detalle(con):
    cursor = con.cursor()
    Query = f"INSERT INTO DETALLE(DNI,Venta_total)\n"
    Query += f"SELECT DATOS.DNI, SUM(PRODUCTOS.Precio) AS Venta_total FROM DATOS,PRODUCTOS,VENTAS\n"
    Query += f"WHERE DATOS.DNI=VENTAS.DNI AND VENTAS.Nombre_producto=PRODUCTOS.Nombre_producto\n"
    Query += f"GROUP BY DATOS.DNI"
    cursor.execute(Query)
    con.commit()

def mostrar_detalle():
    ListaTabla(conexion(),"DETALLE")

def eliminar_detalle(con):
    cursor = con.cursor()
    Query = f"DELETE FROM DETALLE;"
    cursor.execute(Query)
    con.commit()

