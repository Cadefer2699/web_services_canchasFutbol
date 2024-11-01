from flask import Blueprint, request, jsonify
from models.Reserva import Reserva
import json


ws_reserva = Blueprint('ws_reserva', __name__)

@ws_reserva.route('/reserva/registrar', methods=['POST'])
def agregar_reserva(): 
    if request.method == 'POST':
        if {'estudiante_id', 'metodo_pago', 'instructor_id', 'idioma_id', 'disponibilidad_id', 'detalle_reserva'} - set(request.form.keys()): #Validar que el usuario envíe los parámetros requeridos
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'}), 400 #Bad Request
        
        #Leer los parámetros email y clave
        estudiante_id = request.form['estudiante_id']
        metodo_pago = request.form['metodo_pago']
        instructor_id = request.form['instructor_id']
        idioma_id = request.form['idioma_id']
        disponibilidad_id = request.form['disponibilidad_id']
        detalle_reserva = request.form['detalle_reserva']

        #Instanciar un objeto de la clase Reserva
        #---
        obj = Reserva(None, estudiante_id, metodo_pago, instructor_id, idioma_id, disponibilidad_id, detalle_reserva)

        #Ejecutar el método insertar
        resultadoJSONString = obj.insertar()
        #Convertir el JSON string en JSON Object
        resultadoJSONObject = json.loads(resultadoJSONString)

        #imprimir el resultado del servicio web
        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #ok
        else:
            return jsonify(resultadoJSONObject), 500 #ok
