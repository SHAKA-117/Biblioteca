from conexion_mariadb import iniciar_conexion
import random

def Generador_Idusuario(nombre,primer_apellido,segundo_apellido):
    num_random = random.randint(1,9999) 
    abreviatura = str(num_random) + nombre[0] + primer_apellido[0] + segundo_apellido[0]
    return abreviatura

def Generador_Idlibro(nombre):
    texto = nombre.split()
    abreviatura = str(random.randint(1,9999)) 
    
    for palabra in texto:
        abreviatura = abreviatura + palabra[0]
    return abreviatura

def Generador_Idgenero(genero):
    texto = genero.split()
    abreviatura = str(random.randint(1,9999)) 
    for palabra in texto:
        abreviatura = abreviatura + palabra[0]
    return abreviatura

def Generador_IdAutor(autor):
    texto = autor.split()
    abreviatura = str(random.randint(1,9999)) 
    for palabra in texto:
        abreviatura = abreviatura + palabra[0]
    return abreviatura

def Limpiar_Cadena(cadena):
    caracteres_especiales = {"/","#","!","$",";"}
    nueva_cadena = ""
    for cadena_limpia in cadena:
        if cadena_limpia not in caracteres_especiales:
            nueva_cadena = nueva_cadena + cadena_limpia
    return nueva_cadena

def Total_Datos(tabla):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute(f'SELECT COUNT(*) FROM {tabla}')
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Fecha_Entrega(date):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Fecha_Entrega FROM Prestamos WHERE Fecha_Prestamo = %s',(date))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Inicio_sesion(correo):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:    
        cursor.execute("""SELECT Id_Usuario,Contraseña
                          FROM Usuario as U inner join Contactos as C on U.Id_Contacto = C.Id_Contacto 
                          WHERE Email = %s""", (correo)) 
        result = cursor.fetchone()
    conexion.commit()
    conexion.close() 
    return result

def Mostrar_Libros(paginacion,resultado_pagina):
    conexion = iniciar_conexion()
    result =[]
    with conexion.cursor() as cursor:
        cursor.execute(""" SELECT Id_Libro,Nombre_Libro,G.Genero,A.Autor,Estado FROM Libros INNER JOIN Genero AS G 
                       ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A 
                       ON Libros.ID_Autor=A.Id_Autor LIMIT %s,%s """,(paginacion, resultado_pagina))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Total_Busqueda(busqueda):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM Libros WHERE Nombre_Libro LIKE %s',('%' + busqueda + '%'))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Buscar_Libro(busqueda,comienzo, resultado_pagina):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute(""" SELECT Id_Libro,Nombre_Libro,G.Genero,A.Autor,Estado FROM Libros INNER JOIN Genero AS G 
                       ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A 
                       ON Libros.ID_Autor=A.Id_Autor WHERE Nombre_Libro LIKE %s LIMIT %s,%s """,('%' + busqueda + '%',comienzo, resultado_pagina))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Obtener_Libro(id):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute(""" SELECT Id_Libro,Nombre_Libro,G.Genero,A.Autor,Estado FROM Libros INNER JOIN Genero AS G 
                       ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A 
                       ON Libros.ID_Autor=A.Id_Autor WHERE Id_Libro = %s """,(id))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Obtener_IdGenero(genero):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Id_Genero FROM Genero WHERE Genero = %s', (genero))
        result = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return result

def Mostrar_Genero():
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Genero FROM Genero')
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Obtener_IDAutor(autor):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Id_Autor FROM Autor WHERE Autor = %s',(autor))
        result = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return result

def Mostrar_Autor():
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Autor FROM Autor')
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Agregar_Libro(nombre,genero,autor):
    id_libro = Generador_Idlibro(nombre)
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO Libros(Id_Libro,Nombre_Libro,Id_Genero,Id_Autor,Estado) VALUES(%s,%s,%s,%s,%s)', (id_libro,nombre,genero,autor,'Disponible'))
    conexion.commit()
    conexion.close()

def Eliminar_Libro(id):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('DELETE FROM Libros WHERE Id_Libro = %s',(id))
    conexion.commit()
    conexion.close()

def Actualizar_Libro(id,nombre,genero,autor,estado):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
           UPDATE Libros
           SET Nombre_Libro = %s,
               Id_Genero = %s,
               Id_Autor = %s,
               Estado = %s
           WHERE Id_Libro = %s""", (nombre,genero,autor,estado,id))
    conexion.commit()
    conexion.close()

def Obtner_Datos(usuario):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Nombre,Primer_Apellido,Segundo_Apellido,Edad,Correo,Numero_Telefonico FROM Usuario WHERE Id_Usuario = %s',(usuario))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result 

def Contar_Libro(id):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM Libros WHERE Id_Libro = %s',(id))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Obtner_Tipo_Usuario(Id_Usuario):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Tipo_Usuario FROM Usuario WHERE Id_Usuario = %s',(Id_Usuario))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Mostrar_Estudiantes(usuario,comienzo,resultados_pagina):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Id_Usuario,Nombre,Primer_Apellido,Segundo_Apellido FROM Usuario WHERE NOT Id_Usuario = %s LIMIT %s,%s',(usuario,comienzo,resultados_pagina))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Buscar_Usuario(valor_buscado,usuario,comienzo,resultados_pagina):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Id_Usuario,Nombre,Primer_Apellido,Segundo_Apellido FROM Usuario WHERE NOT Id_Usuario = %s && Nnombre %s% LIMIT %s,%s',('%'+ valor_buscado + '%',usuario,comienzo,resultados_pagina))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Contar_Usuario(id):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM Usuario WHERE Id_Usuario = %s',(id))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Obtener_Estudiante(id):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Id_Usuario,Nombre,Primer_Apellido,Segundo_Apellido,Edad,Correo,Numero_Telefonico FROM Usuario WHERE Id_Usuario = %s',(id))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Registrar_Usuario(usuario,contrasena,nombre,primer_apellido,segundo_apellido,edad,correo,numero_telefonico,tipo_usuario):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO Usuario(Id_Usuario,Contraseña,Nombre,
        Primer_Apellido,Segundo_Apellido,Edad,Correo,Numero_Telefonico,Tipo_Usuario) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(usuario,contrasena,nombre,primer_apellido,segundo_apellido,edad,correo,numero_telefonico,tipo_usuario))
        cursor.fetchall()
    conexion.commit()
    conexion.close()

def Comprobar_Correo(correo):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT Correo FROM Usuario WHERE Correo = %s',(correo))
        result = cursor.fetchone()
    conexion.commit()
    conexion.close()
    return result

def Datos_Alquilar(Id_Libro):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT Nombre_Libro,G.Genero,A.Autor FROM Libros INNER JOIN Genero AS G 
                       ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A 
                       ON Libros.ID_Autor=A.Id_Autor WHERE Id_Libro = %s """,(Id_Libro))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Prestamo_Libro(usuario,Id_Libro,fecha_prestamo,fecha_final):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO Prestamos(Id_Libro,Id_Usuario,Fecha_Prestamo,Fecha_Entrega) VALUES (%s,%s,%s,%s)
        """,(Id_Libro,usuario,fecha_prestamo,fecha_final))
        cursor.fetchall()
        cursor.execute("""UPDATE Libros 
                         SET Estado = %s
                         WHERE Id_Libro = %s
                       """,('Ocupado',Id_Libro))
        cursor.fetchall()
    conexion.commit()
    conexion.close()

def Lista_Prestamos(usuario):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT Libros.Id_Libro, Nombre_Libro, G.Genero, A.Autor
                          FROM Libros INNER JOIN Genero AS G ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A
                          ON Libros.ID_Autor=A.Id_Autor INNER JOIN Prestamos AS P ON Libros.Id_Libro=P.Id_Libro INNER JOIN
                          Usuario AS U ON P.Id_Usuario=U.Id_Usuario
                          WHERE U.Id_Usuario = %s""",(usuario))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result

def Total_Libros_Prestados(usuario):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute( """SELECT COUNT(*)
                          FROM Libros INNER JOIN Genero AS G ON Libros.Id_Genero = G.Id_Genero INNER JOIN Autor AS A
                          ON Libros.ID_Autor=A.Id_Autor INNER JOIN Prestamos AS P ON Libros.Id_Libro=P.Id_Libro INNER JOIN
                          Usuario AS U ON P.Id_Usuario=U.Id_Usuario
                          WHERE U.Id_Usuario = %s""",(usuario))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]

def Devolucion_Libro(Id_Libro):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""DELETE FROM Prestamos WHERE Id_Libro = %s  """,(Id_Libro))
        cursor.execute("""UPDATE Libros 
                         SET Estado = %s
                         WHERE Id_Libro = %s
                       """,('Disponible',Id_Libro))
    conexion.commit()
    conexion.close()

def Usuarios_Telegram(fecha):
    conexion = iniciar_conexion()
    result = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT Id_Telegram 
                          FROM Contactos AS C INNER JOIN Usuario AS U ON C.Id_Contacto = U.Id_Contacto INNER JOIN
                          Prestamos As P ON U.Id_Usuario = P.Id_Usuario
                          WHERE Fecha_Prestamo = %s
        """,(fecha))
        result = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return result[0]
