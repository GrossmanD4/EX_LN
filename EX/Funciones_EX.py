from Funciones_SQL import *
from datetime import datetime, date, time
#Funciones Generales
def fecha():
    d = datetime.now()
    m = d.month
    y = d.year
    i = d.day
    return f"{i}-{m}-{y}"

def datos(con):
    cursor=con.cursor()
    Query="CREATE TABLE IF NOT EXISTS DATOS( "
    Query+="Codigo_A VARCHAR(5) PRIMARY KEY, "
    Query+="Nombre_A VARCHAR(20),"
    Query+="Raza VARCHAR(20), "
    Query+="Edad INT DEFAULT 0, "
    Query+="Peso INT DEFAULT 0) "
    cursor.execute(Query)
    con.commit()

def datos_asistente(con):
    cursor=con.cursor()
    Query="CREATE TABLE IF NOT EXISTS DATOSA( "
    Query+="DNI VARCHAR(8) PRIMARY KEY, "
    Query+="Codigo VARCHAR(5), "
    Query+="Nombre VARCHAR(20), "
    Query+="Edad INT DEFAULT 18) "
    cursor.execute(Query)
    con.commit()

def datos_proceso(con):
    cursor=con.cursor()
    Query="CREATE TABLE IF NOT EXISTS PROCESO( "
    Query+="N VARCHAR (5), "
    Query+="DNI VARCHAR(8), "
    Query+="Codigo_A VARCHAR(5), "
    Query+="Fecha_proceso date, "
    Query+="Costo_atencion INT DEFAULT 0,"
    Query+="Pago BLOB,"
    Query+="PRIMARY KEY(N,DNI,Codigo_A)"
    Query+="FOREIGN KEY(DNI) REFERENCES DATOSA(DNI),"
    Query+="FOREIGN KEY(Codigo_A) REFERENCES DATOS(Codigo_A))"
    cursor.execute(Query)
    con.commit()

def insercion_base_datos(con):
    cursor=con.cursor()
    cursor.execute("SELECT * FROM DATOS")
    validador=cursor.fetchone()
    if validador:
        pass
    else:
        lista_datos=[("29125","Clayton","Shnauzer",2,10),("28100","Tetsu","Bulldog",3,34),("26505","Teodoro","Chitzu",6,23)]
        cursor.executemany("INSERT INTO DATOS VALUES(?,?,?,?,?);",lista_datos)
        con.commit()

def insercion_base_asistente(con):
    cursor=con.cursor()
    cursor.execute("SELECT * FROM DATOSA")
    validador=cursor.fetchone()
    if validador:
        pass
    else:
        lista_datos=[("72949694","20052","Grossman",17),("00493656","20005","Edwi",54),("12345678","12345","Paola",42)]
        cursor.executemany("INSERT INTO DATOSA VALUES(?,?,?,?);",lista_datos)
        con.commit()

def mostrar_dni(con):
    cur=con.cursor()
    cur.execute("SELECT DNI FROM DATOSA")
    sentencias=cur.fetchall()
    for x in sentencias:
        print(f">{x[0]}")

def mostrar_cod_a(con):
    cur=con.cursor()
    cur.execute("SELECT Codigo_A FROM DATOS")
    sentencias=cur.fetchall()
    for x in sentencias:
        print(f">{x[0]}")

def obt_DNI(con):
    mostrar_dni(con)
    DNI=input("Ingrese su DNI por favor --> ")
    cursor=con.cursor()
    cursor.execute(f"SELECT * FROM DATOSA WHERE DNI={DNI}")
    validacion=cursor.fetchall()
    while len(validacion)!=True:
        DNI=input("Error al ingresar, trate de nuevo --> ")
        cursor.execute(f"SELECT * FROM DATOSA WHERE DNI={DNI}")
        validacion=cursor.fetchall()
    return DNI

def obt_CodA(con):
    mostrar_cod_a(con)
    Codigo_A=input("Ingrese el código de la mascota --> ")
    cursor=con.cursor()
    cursor.execute(f"SELECT * FROM DATOS WHERE Codigo_A={Codigo_A}")
    validacion=cursor.fetchall()
    while len(validacion)!=True:
        Codigo_A=input("Error al ingresar, trate de nuevo --> ")
        cursor.execute(f"SELECT * FROM DATOS WHERE Codigo_A={Codigo_A}")
        validacion=cursor.fetchall()
    return Codigo_A

def obt_Cod_AN(con):
    Codigo_A=input("Ingrese el nuevo código de la mascota --> ")
    cursor=con.cursor()
    cursor.execute(f"SELECT * FROM DATOS WHERE Codigo_A={Codigo_A}")
    validacion=cursor.fetchall()
    while len(validacion)==True:
        Codigo_A=input("Error al ingresar, trate de nuevo --> ")
        cursor.execute(f"SELECT * FROM DATOS WHERE Codigo_A={Codigo_A}")
        validacion=cursor.fetchall()
    return Codigo_A

def obt_Costo():
    Costo_atencion=float(input("Ingrese el costo total de la atención. -->"))
    while Costo_atencion<=0:
        Costo_atencion=float(input("Error al ingresar el costo -->"))
    return Costo_atencion

def obt_nombre_a():
    nombre=input("Ingrese el nombre de su mascota --> ")
    while len(nombre)==0:
        nombre=input("Error al ingresar el nombre -->")
    return nombre

def obt_raza():
    raza=input("Ingrese la raza de su mascota -->")
    while len(raza)==0:
        raza=input("Error al ingresar la raza -->")
    return raza

def obt_edad():
    edad=round(float(input("Ingrese la edad de su mascota -->")))
    while edad<=0:
        edad=round(float(input("Error al ingresar la edad -->")))
    return edad

def obt_peso():
    peso=round(float(input("Ingrese el peso de su mascota -->")))
    while peso<=0:
        peso=round(float(input("Error al ingresar el peso -->")))
    return peso

#Funciones llamado
def tabla_datos(cur):
    fo = open("DATOS.txt","w")
    cur.execute("SELECT * FROM DATOS")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")

def tabla_datosa(cur):
    fo = open("DATOSA.txt","w")
    cur.execute("SELECT * FROM DATOSA")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")        

def tabla_procesos_completos(cur):
    Query="SELECT PROCESO.N,PROCESO.DNI,DATOSA.Nombre,PROCESO.Codigo_A,DATOS.Nombre_A,Fecha_proceso,Costo_atencion,Pago FROM DATOS,DATOSA,PROCESO " 
    Query+="WHERE PROCESO.DNI=DATOSA.DNI AND PROCESO.Codigo_A=DATOS.Codigo_A"
    cur.execute(Query)
    fo = open("PROCESOS.txt","w")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")

def tabla_sin_pagar(cur):
    Query="SELECT PROCESO.N,PROCESO.DNI,DATOSA.Nombre,PROCESO.Codigo_A,DATOS.Nombre_A,Fecha_proceso,Costo_atencion,Pago FROM DATOS,DATOSA,PROCESO " 
    Query+="WHERE PROCESO.DNI=DATOSA.DNI AND PROCESO.Codigo_A=DATOS.Codigo_A AND Pago=0"
    cur.execute(Query)
    fo = open("SINPAGAR.txt","w")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")

def tabla_pagadas(cur):
    Query="SELECT PROCESO.N,PROCESO.DNI,DATOSA.Nombre,PROCESO.Codigo_A,DATOS.Nombre_A,Fecha_proceso,Costo_atencion,Pago FROM DATOS,DATOSA,PROCESO " 
    Query+="WHERE PROCESO.DNI=DATOSA.DNI AND PROCESO.Codigo_A=DATOS.Codigo_A AND Pago=1"
    cur.execute(Query)
    fo = open("PAGADOS.txt","w")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")

def tabla_precio_codigo(cur):
    codigo=obt_CodA(conexion())
    Query="SELECT PROCESO.Codigo_A,DATOS.Nombre_A,sum(PROCESO.Costo_atencion) " 
    Query+=f"FROM DATOS,PROCESO WHERE DATOS.Codigo_A=PROCESO.Codigo_A AND Pago=0 AND PROCESO.Codigo_A={codigo} "
    Query+="GROUP BY PROCESO.Codigo_A"
    cur.execute(Query)
    fo = open("PAGADOS.txt","w")
    sentencias=cur.fetchall()
    op=input("¿Desea guardar los resultados en un archivo externo? --> ").lower()
    while op!="si" and op!="no":
        op=input("Ingrese una respuesta válida --> ").lower()
    if op=="si":
        for x in sentencias:
            print(f">{x}")
            fo.write(str(x))
    else:
        for x in sentencias:
            print(f">{x}")

#Funciones menu principal
#Este es el menu que se usara para obtener la elección del usuario segun los números
def menu_opc():
    opciones={"1":"Mostrar registro completo de los animales",
              "2":"Mostrar registro completo de los asistentes",
              "3":"Mostrar lista de procesos completos", 
              "4":"Deuda pendiente según el código de su mascota",
              "5":"Mostrar deudas que no se han pagado", 
              "6":"Mostrar deudas que se han pagado"} 
    for x,y in opciones.items():
        print(x,y)
    eleccion=input("¿Que desea mostrar por pantalla? --> ")
    while eleccion not in opciones.keys():
        eleccion=input("Ingrese una opción válida por favor --> ")   
    return eleccion

#Este menú se utilizara para realizar las consultas
def menu_consultas(con):
    cursor=con.cursor()
    eleccion=menu_opc()

    if eleccion=="1":
        tabla_datos(cursor)
    
    elif eleccion=="2":
        tabla_datosa(cursor)

    elif eleccion=="3":
        tabla_procesos_completos(cursor)

    elif eleccion=="4":
        tabla_precio_codigo(cursor)

    elif eleccion=="5":
        tabla_sin_pagar(cursor)

    elif eleccion=="6":
        tabla_pagadas(cursor)


#Inserta Valores base a las tablas
def insercion_base():
    con=conexion()
    insercion_base_asistente(con)
    insercion_base_datos(con)

#Crea tablas base si no existen
def creación_tablas():
    con=conexion()
    datos(con)
    datos_asistente(con)
    datos_proceso(con)

#Insertar datos a la tabla proceso
def insercion_proceso(con):
    cursor=con.cursor()
    Nventa=input("Ingrese el número de atención -->")
    DNI=obt_DNI(con)
    Codigo_A=obt_CodA(con) 
    Fecha_proceso=fecha()
    Costo_atencion=obt_Costo()
    print("¿El cliente canceló el pago? -->")
    rpt=input("--> ").lower()
    while rpt!="no" and rpt!="si":
        rpt=input("--> ").lower()
    if rpt=="si":
        Pago=True
    else:
        Pago=False
    cursor.execute(f"INSERT INTO PROCESO VALUES ({Nventa},{DNI},{Codigo_A},'{Fecha_proceso}',{Costo_atencion},{Pago})")
    con.commit()

#Registrar nueva mascota+
def insercion_mascota(con):
    cur=con.cursor()
    codigo=obt_Cod_AN(con)
    nombre=obt_nombre_a()
    raza=obt_raza()
    edad=obt_edad()
    peso=obt_peso()
    cur.execute(f"INSERT INTO DATOS VALUES ('{codigo}','{nombre}','{raza}','{edad}','{peso}')")
    con.commit()

#Eliminar datos
def eliminardatos(con):
    print("Indique de qué tabla eliminará un registro:")
    imprimirTabla(con)
    eleccion=input("--> ").upper()
    while eleccion!="DATOS" and eleccion!="DATOSA" and eleccion!="PROCESO":
        eleccion=input("--> ").upper()
    if eleccion=="DATOS":
        eliminarTabla(con,"Codigo_A","DATOS")
    if eleccion=="DATOSA":
        eliminarTabla(con,"DNI","DATOSA")
    if eleccion=="PROCESO":
        eliminarTabla(con,"N","PROCESO")

#Modificar Datos
def Modificardatos(con):
    print("Indique de qué tabla se modificará un registro:")
    imprimirTabla(con)
    eleccion=input("--> ").upper()
    while eleccion!="DATOS" and eleccion!="DATOSA" and eleccion!="PROCESO":
        eleccion=input("--> ").upper()
    if eleccion=="DATOS":
        modificarTabla(con,"Codigo_A","DATOS")
    if eleccion=="DATOSA":
        modificarTabla(con,"DNI","DATOSA")
    if eleccion=="PROCESO":
        modificarTabla(con,"N","PROCESO")



#Opciones
def opc_02():
    print("''''''")
    print("MENU VETERINARIA GOTITAS DEL SABER:")
    oc={"1":"Abrir el menú de consultas", "2":"Insertar una nueva mascota en caso no estar registrada"
        ,"3":"Insertar datos consulta","4":"Eliminar registros","5":"Modificar Tabla",
        "6":"Terminar el programa"}
    for x,y in oc.items():
        print(f">{x,y}")
    opc=input("Digite su elección --> ")
    while opc not in oc.keys():
        opc=input("Error --> ")
    return opc

#Menu Principal
def menu():
    creación_tablas()
    insercion_base
    while True:
        con=conexion()
        opc = opc_02()
        if opc == "1":
            menu_consultas(con)
        elif opc == "2":
            insercion_mascota(con)
        elif opc == "3":
            insercion_proceso(con)
        elif opc=="4": 
            eliminardatos(con)
        elif opc == "5":
            Modificardatos(con)
        else: 
            break