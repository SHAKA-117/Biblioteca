from flask import Flask, flash, render_template, request, redirect, session, url_for
from datetime import datetime
from datetime import timedelta

from werkzeug.wrappers import response
import Controlador_SQL, os, requests
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')

app = Flask(__name__)

app.secret_key = 'myscretkey'

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('Inicio'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Principal')
def Principal():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario) 
        if tipo_usuario[0] == 1:
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        comienzo = 0
        indice = 0

        if 'comienzo' in request.args:
            comienzo = int(request.args['comienzo'])

        if 'indice' in request.args:
            indice = int(request.args['indice'])
            comienzo = indice * 5
            
        navegacion = Controlador_SQL.Total_Datos('Libros')
        resultados_pagina = round(navegacion[0] / 5)
        siguiente = comienzo + 5
        anterior = comienzo - 5
        resultados_por_pagina = 5
        result = Controlador_SQL.Mostrar_Libros(comienzo,resultados_por_pagina)
        nombre_buscado = ""

        if "Busqueda" in request.args:
            nombre_buscado = request.args["Busqueda"]
            navegacion = Controlador_SQL.Total_Busqueda(nombre_buscado)
            resultados_pagina = round(navegacion[0] / 5)
            result = Controlador_SQL.Buscar_Libro(nombre_buscado,comienzo,resultados_por_pagina)
        
        return render_template("principal.html", result = result, valor_anterior = anterior, valor_siguiete = siguiente, valor_buscado = nombre_buscado,resultado_pagina = resultados_pagina, total_datos = navegacion[0])

@app.route('/Inicio_Adminitrador')
def Inicio_Adminitrador():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)    

        if tipo_usuario[0] == 1:
            comienzo = 0
            indice = 0

            if 'comienzo' in request.args:
                comienzo = int(request.args['comienzo'])

            if 'indice' in request.args:
                indice = int(request.args['indice'])
                comienzo = indice * 5

            navegacion = Controlador_SQL.Total_Datos('Libros')
            resultados_pagina = round(navegacion[0] / 5)
            siguiente = comienzo + 5
            anterior = comienzo - 5
            resultados_por_pagina = 5
            result = Controlador_SQL.Mostrar_Libros(comienzo,resultados_por_pagina)
            nombre_buscado = ""

            if "Busqueda" in request.args:
                nombre_buscado = request.args["Busqueda"]
                usuario = session['usuario']
                navegacion = Controlador_SQL.Total_Busqueda(nombre_buscado)
                resultados_pagina = round(navegacion[0] / 5)
                result = Controlador_SQL.Buscar_Usuario(nombre_buscado,usuario,comienzo,resultados_por_pagina)
            return render_template("admin/Inicio.html", result = result, valor_anterior = anterior, valor_siguiete = siguiente, valor_buscado = nombre_buscado,resultado_pagina = resultados_pagina, total_datos = navegacion[0])
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Nuevo_Libro')
def Nuevo_Libro():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)    

        if tipo_usuario[0] == 1:
            Controlador_SQL.Generador_Idlibro("El Monje Loco")
            result = Controlador_SQL.Mostrar_Genero()
            autor = Controlador_SQL.Mostrar_Autor()
            return render_template('admin/agregar.html', result = result, autor = autor)
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal')) 

@app.route('/Error')
def Error():
    return render_template('error.html')

@app.route('/Sesiones')
def Sesiones():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)

        if tipo_usuario[0] == 1:
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return render_template('sesion.html')

@app.route('/Cerrar_Sesion')
def Cerrar_Sesion():
    if 'usuario' in session:
        session.clear()
        #session.pop('usuario')
        return redirect(url_for('Principal'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Inicio_sesion', methods=['POST'])
def Inicio_sesion():
    if request.method == 'POST':
        correo = request.form['Correo'] 
        correo = Controlador_SQL.Limpiar_Cadena(correo)
        result = Controlador_SQL.Inicio_sesion(correo)
        if result is None :
            flash('Usuario o Contraseña incorrectos')
            return redirect(url_for('Sesiones'))
        else:
            contrasena = request.form['Contrasena']
            if check_password_hash(result[1],contrasena):
                tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(result[0])
                if tipo_usuario[0] == 1:
                    session['usuario'] = result[0]
                    return redirect(url_for('Inicio_Adminitrador'))
                elif tipo_usuario[0] == 2:
                    session['usuario'] = result[0]
                    return redirect(url_for('Inicio_Usuario'))
                else:
                    flash('Usuario o Contraseña incorrectos')
                    return redirect(url_for('Sesiones'))
            else:
                flash('Usuario o Contraseña incorrectos')
                return redirect(url_for('Sesiones'))
    else:
        return redirect(url_for('error'))

@app.route('/Registro')
def Registro():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            session['usuario'] = usuario
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            session['usuario'] = usuario
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return render_template('registrar_usuario.html')

@app.route('/Registrar_Usuario', methods=['POST'])
def Registrar_Usuario():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        if request.method == 'POST':
            correo = request.form['Correo']
            correo = Controlador_SQL.Limpiar_Cadena(correo)
            comprobar = Controlador_SQL.Comprobar_Correo(correo)
            if comprobar is None:
                contrasena = request.form['Contrasena']
                contrasena = Controlador_SQL.Limpiar_Cadena(contrasena)
                nombre = request.form['Nombre']
                nombre = Controlador_SQL.Limpiar_Cadena(nombre)
                primer_apellido = request.form['Primer_Apellido']
                primer_apellido = Controlador_SQL.Limpiar_Cadena(primer_apellido)
                segundo_apellido = request.form['Segundo_Apellido']
                segundo_apellido = Controlador_SQL.Limpiar_Cadena(segundo_apellido)
                edad = request.form['Edad']
                edad = Controlador_SQL.Limpiar_Cadena(edad)
                numero_telefonico = request.form['Numero_Telefonico']
                numero_telefonico = Controlador_SQL.Limpiar_Cadena(numero_telefonico)
                usuario = Controlador_SQL.Generador_Idusuario(nombre,primer_apellido,segundo_apellido) 
                cifrado = generate_password_hash(contrasena, method='pbkdf2:sha256')
                Controlador_SQL.Registrar_Usuario(usuario,cifrado,nombre,primer_apellido,segundo_apellido,edad,correo,numero_telefonico,2)
                flash('Usuario registrado exitosamente')
                return redirect(url_for('Registro'))
            else:
                flash('El usuario ya existe')
                return redirect(url_for('Registro'))
        else:
            return redirect(url_for('Error'))

@app.route('/Agregar_Libro', methods=['POST'])
def Agregar_Libro():
    if 'usuario' in session:
        usuario = session['Usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            if request.method == 'POST':
                nombre = request.form['Nombre']
                nombre = Controlador_SQL.Limpiar_Cadena(nombre)
                genero = request.form.get('Genero')
                genero = Controlador_SQL.Limpiar_Cadena(genero)
                autor = request.form.get('Autor')
                autor = Controlador_SQL.Limpiar_Cadena(autor)
                genero = Controlador_SQL.Obtener_IdGenero(genero)
                autor = Controlador_SQL.Obtener_IDAutor(autor)    
                Controlador_SQL.Agregar_Libro(nombre,genero,autor)
                flash('Libro agregado exitorasamente')
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('principal'))

@app.route('/Eliminar/<string:id>')
def Eliminar(id):
    id = Controlador_SQL.Limpiar_Cadena(id)
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            id = Controlador_SQL.Limpiar_Cadena(id)
            Controlador_SQL.Eliminar_Libro(id)
            flash('Libro eliminado exitorasamente')
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('principal'))
    
@app.route('/Editar/<string:id>')
def Editar(id):
    id = Controlador_SQL.Limpiar_Cadena(id)
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        id = Controlador_SQL.Limpiar_Cadena(id)

        if tipo_usuario[0] == 1:
            cont_libro = Controlador_SQL.Contar_Libro(id)
            cont_usuario = Controlador_SQL.Contar_Usuario(id)
            if cont_libro[0] == 1:
                result = Controlador_SQL.Obtener_Libro(id)
                genero = Controlador_SQL.Mostrar_Genero()
                autor = Controlador_SQL.Mostrar_Autor()
                return render_template('admin/editar.html', result = result[0], genero = genero, autor = autor)
            elif cont_usuario[0] == 2:
                result = Controlador_SQL.Obtener_Estudiante(id)
                return render_template('admin/editar_usuario.html', result = result[0])
            else:
                return redirect(url_for('Error'))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('principal'))

@app.route('/Editar_Libro/<string:id>', methods=['POST'])
def Editar_Libro(id):
    id = Controlador_SQL.Limpiar_Cadena(id)
    if 'usuario' in  session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        id = Controlador_SQL.Limpiar_Cadena(id)

        if tipo_usuario == 1:
            if request.method == 'POST':
                nombre = request.form['Nombre']
                nombre = Controlador_SQL.Limpiar_Cadena(nombre)
                genero = request.form.get('Genero')
                genero = Controlador_SQL.Limpiar_Cadena(genero)
                autor = request.form.get('Autor')
                autor = Controlador_SQL.Limpiar_Cadena(autor)
                genero = Controlador_SQL.Obtener_IdGenero(genero)
                autor = Controlador_SQL.Obtener_IDAutor(autor)
                estado = request.form['Estado']
                estado = Controlador_SQL.Limpiar_Cadena(estado)
                Controlador_SQL.Actualizar_Libro(id,nombre,genero,autor,estado)
                flash('Libro actualizado exitorasamente')
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Perfil/')
def Perfil():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)

        if tipo_usuario[0] == 1:
            usuario = session['usuario']
            result = Controlador_SQL.Obtner_Datos(usuario)
            return render_template('admin/perfil.html', result = result[0])
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error')) 
    else:
        return redirect(url_for('Principal'))

@app.route('/Lista_Usuario')
def Lista_Usuario():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)

        if tipo_usuario[0] == 1:
            comienzo = 0
            indice = 0

            if 'comienzo' in request.args:
                comienzo = int(request.args['comienzo'])

            if 'indice' in request.args:
                indice = int(request.args['indice'])
                comienzo = indice * 5

            navegacion = Controlador_SQL.Total_Datos('Usuario')
            usuario = session['usuario']
            siguiente = comienzo + 5
            anterior = comienzo - 5
            resultados_por_pagina = 5
            result = Controlador_SQL.Mostrar_Estudiantes(usuario,comienzo,resultados_por_pagina)
            resultados_pagina = round(navegacion[0] / 5)

            nombre_buscado = ""
            if "Busqueda" in request.args:
                nombre_buscado = request.args["Busqueda"]
                nombre_buscado = Controlador_SQL.Limpiar_Cadena(nombre_buscado)
                navegacion = Controlador_SQL.Total_Busqueda(nombre_buscado)
                resultados_pagina = round(navegacion[0] / 5)
                result = Controlador_SQL.Buscar_Libro(nombre_buscado,comienzo,resultados_por_pagina)
            return render_template('admin/lista_usuario.html',result = result, valor_anterior = anterior, valor_siguiete = siguiente, valor_buscado = nombre_buscado,resultado_pagina = resultados_pagina, total_datos = len(result))
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Inicio_Usuario')
def Inicio_Usuario():
    if 'usuario' in session:
        comienzo = 0
        indice = 0
        
        if 'comienzo' in request.args:
            comienzo = int(request.args['comienzo'])
        
        if 'indice' in request.args:
            indice = int(request.args['indice'])
            comienzo = indice * 5
        
        navegacion = Controlador_SQL.Total_Datos('Libros')
        resultados_pagina = round(navegacion[0] / 5)
        siguiente = comienzo + 5
        anterior = comienzo - 5
        resultados_por_pagina = 5
        result = Controlador_SQL.Mostrar_Libros(comienzo,resultados_por_pagina)

        nombre_buscado = ""
        
        if "Busqueda" in request.args:
            nombre_buscado = request.args["Busqueda"]
            nombre_buscado = Controlador_SQL.Limpiar_Cadena(nombre_buscado)
            navegacion = Controlador_SQL.Total_Busqueda(nombre_buscado)
            resultados_pagina = round(navegacion[0] / 5)
            result = Controlador_SQL.Buscar_Libro(nombre_buscado,comienzo,resultados_por_pagina)
        return render_template('usuarios/Inicio.html',result = result, valor_anterior = anterior, valor_siguiete = siguiente, valor_buscado = nombre_buscado,resultado_pagina = resultados_pagina, total_datos = navegacion[0])
    else:
        return redirect(url_for('Principal'))

@app.route('/Alquilar/<string:Id_Libro>')
def Alquilar(Id_Libro):
    Id_Libro = Controlador_SQL.Limpiar_Cadena(Id_Libro)
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2:
            fecha_actual = datetime.now()
            fecha_final = fecha_actual + timedelta(days=7) 
            fecha_actual = fecha_actual.strftime('%d-%m-%Y')
            fecha_final = fecha_final.strftime('%d-%m-%Y')
            result = Controlador_SQL.Datos_Alquilar(Id_Libro)
            return render_template('usuarios/alquilar.html',fecha_inicio = fecha_actual, fecha_final = fecha_final, result = result, Id_Libro = Id_Libro)
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Alquilar_Libro/<string:Id_Libro>',methods=['POST'])
def Alquilar_Libro(Id_Libro):
    Id_Libro = Controlador_SQL.Limpiar_Cadena(Id_Libro)
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            return redirect(url_for('Inicio_Adminitrador'))
        elif tipo_usuario[0] == 2: 
            fecha_prestamo = request.form.get('Inicio_Fecha2') 
            fecha = datetime.strptime(str(fecha_prestamo), "%d-%m-%Y")
            fecha_prestamo = fecha.strftime("%Y-%m-%d")
            fecha_final = request.form.get('Fin_Fecha2')
            fecha_fin = datetime.strptime(str(fecha_final), "%d-%m-%Y") 
            fecha_final = fecha_fin.strftime("%Y-%m-%d")
            Controlador_SQL.Prestamo_Libro(usuario,Id_Libro,fecha_prestamo,fecha_final)
            flash('Libro reservado con exito')
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Lista_Prestamo/<string:Id_Usuario>')
def Lista_Prestamo(Id_Usuario):
    Id_Usuario = Controlador_SQL.Limpiar_Cadena(Id_Usuario)
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
        if tipo_usuario[0] == 1:
            comienzo = 0

            nombre_usuario = Controlador_SQL.Obtner_Datos(Id_Usuario)
            result = Controlador_SQL.Lista_Prestamos(Id_Usuario)
            navegacion = Controlador_SQL.Total_Libros_Prestados(Id_Usuario)
            resultados_pagina = round(navegacion[0] / 5)
            siguiente = comienzo + 5
            anterior = comienzo - 5
            resultados_por_pagina = 5
            nombre_buscado = ""

            if "Busqueda" in request.args:
                nombre_buscado = request.args["Busqueda"]
                nombre_buscado = Controlador_SQL.Limpiar_Cadena(nombre_buscado)
                navegacion = Controlador_SQL.Total_Busqueda(nombre_buscado)
                resultados_pagina = round(navegacion[0] / 5)
                result = Controlador_SQL.Buscar_Libro(nombre_buscado,comienzo,resultados_por_pagina)
        
            return render_template('admin/Lista_Prestamo.html', result = result, valor_anterior = anterior, valor_siguiete = siguiente, valor_buscado = nombre_buscado,resultado_pagina = resultados_pagina, total_datos = navegacion[0],nombre_usuario = nombre_usuario[0])#hora = datetime(str(fecha),9,41,00)
        elif tipo_usuario[0] == 2:
            return redirect(url_for('Inicio_Usuario'))
        else:
            return redirect(url_for('Error'))
    else:
        return redirect(url_for('Principal'))

@app.route('/Devolver_Libro/<string:Id_Libro>')
def Devolver_Libro(Id_Libro):
     Id_Libro = Controlador_SQL.Limpiar_Cadena(Id_Libro)
     if 'usuario' in session:
         usuario = session['usuario']
         tipo_usuario = Controlador_SQL.Obtner_Tipo_Usuario(usuario)
         if tipo_usuario[0] == 1:
             Controlador_SQL.Devolucion_Libro(Id_Libro)
             flash('Libro devuelto con exito')
             return redirect(url_for('Inicio_Adminitrador'))
         elif tipo_usuario[0] == 2:
             return redirect(url_for('Inicio_Usuario'))
         else:
             return redirect(url_for('Error'))
     else:
        return redirect(url_for('Principal'))

#def Enviar_Mensaje():
#    fecha_actual = datetime.now()
#    fecha = Controlador_SQL.Fecha_Entrega(fecha_actual.date())
#    Id_Usuarios = Controlador_SQL.Usuarios_Telegram(fecha[0])
#    mensaje = 'Tienes que devolver el libro'
#    url = f'https://api.telegram.org/bot{TOKEN_BOT}/sendMessage'
#    for usuario in Id_Usuarios:
#        payload = {
#            'chat_id': usuario,
#            'text': mensaje
#            }
#        requests.post(url, data=payload)

URL = f'https://api.telegram.org/bot{TOKEN_BOT}/'
WEBHOOK_URL = 'http://127.0.0.1:5000/webhook'

def Enviar_Mensaje(chat_id,text):
    url = URL + 'sendMessage'
    payload = {
            'chat_id': chat_id,
            'text': text
           }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    mensaje_text = data['message']['text']

    print(chat_id)

    if mensaje_text == '/id':
        Enviar_Mensaje(chat_id, '!HOLI!, te escucho')
    else:
        Enviar_Mensaje(chat_id, 'No reconosco ese comando')

    return '', 200

def Enviar_Webhook():
    webhook_url = URL + 'setWebhook'
    payload = {'url': WEBHOOK_URL}
    response = requests.post(webhook_url, json=payload)
    return response.json()

print(Enviar_Webhook())

#scheduler = BackgroundScheduler()
#scheduler.add_job(Enviar_Mensaje, 'cron', hour = 8, minute=48)
#scheduler.start()

if __name__ == "__nage__":
    app.run(debug=True) 

