from flask import Blueprint, request, jsonify
from models.Sesion import Sesion
import json
import jwt #pyjwt
import datetime
from config import SecretKey

#Crear un módulo para gestionar los endpoints relacionados a la sesión del usuario
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear un endpoint para el inicio de sesión
@ws_sesion.route('/usuario/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if {'email', 'clave'} - set(request.form.keys()): #Validar que el usuario envíe los parámetros requeridos
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'}), 400 #Bad Request
        
        #Leer los parámetros email y clave
        email = request.form['email']
        clave = request.form['clave']

        #Instanciar un objeto de la clase Sesion
        obj = Sesion(email, clave)

        #Ejecutar el método iniciar sesión
        resultadoJSONString = obj.iniciarSesion()

        #Convertir el JSON string en JSON Object
        resultadoJSONObject = json.loads(resultadoJSONString)

        #Validar los datos del resultado enviado por el método iniciar sesión
        if resultadoJSONObject['status'] == True:
            #Almacenar el ID del usuario en una variable para enviarlo en el token
            usuarioID = resultadoJSONObject['data']['id']

            #Generar y otorgar el token al usuario que ha iniciado sesión satisfactoriamente
            token = jwt.encode({'usuarioID': usuarioID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)}, SecretKey.JWT_SECRET_KEY)

            #Incorporar el token en los datos de la sesión del usuario
            resultadoJSONObject['data']['token'] = token

            #Actualizar el token del usuario en la BD
            resultadoActualizarTokenJSONObject = json.loads(obj.actualizarToken(token, usuarioID))
            if resultadoActualizarTokenJSONObject['status'] == False: #Ocurrió un error al actualizar el token
                return jsonify(resultadoActualizarTokenJSONObject), 500 #Internal Server Error

            #Imprimir la respuesta del servicio web
            return jsonify(resultadoJSONObject), 200 #ok
        else: #Credenciales fueron incorrectas o el estado del usuario es inactivo
            #Imprimir la respuesta del servicio web
            return jsonify(resultadoJSONObject), 401 #Unauthorized
        

        



