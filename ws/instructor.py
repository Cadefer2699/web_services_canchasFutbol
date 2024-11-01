from flask import Blueprint, request, jsonify
from models.Instructor import Instructor
import json
import validarToken as vt

ws_instructor = Blueprint('ws_instructor', __name__)

@ws_instructor.route('/instructor/catalogo/<int:idioma_id>/<int:instructor_id>/<int:disponibilidad_id>/<string:fecha>', methods=['GET'])
@ws_instructor.route('/instructor/catalogo/<int:idioma_id>/<int:instructor_id>/<int:disponibilidad_id>', methods=['GET'])
#@vt.validar
def catalogo(idioma_id, instructor_id, disponibilidad_id, fecha=None):
    if request.method == 'GET':
        if not idioma_id:
            return jsonify({'status': False, 'data':None, 'message': 'Falta id de idioma'}), 400 #Bad Request
        
        if not instructor_id:
            if instructor_id != 0:
                return jsonify({'status': False, 'data':None, 'message': 'Falta id de instructor'}), 400 #Bad Request
        if not disponibilidad_id:
            if disponibilidad_id != 0:
                return jsonify({'status': False, 'data':None, 'message': 'Falta id de disponibilidad'}), 400 #Bad Request
        
        obj = Instructor()

        resultadoInstructorJSONObject = json.loads(obj.catalogo(idioma_id, instructor_id, disponibilidad_id, fecha))

        #imprimir el resultado del servicio web
        if resultadoInstructorJSONObject['status'] == True:
            return jsonify(resultadoInstructorJSONObject), 200 #ok
        else:
            return jsonify(resultadoInstructorJSONObject), 500 #Error