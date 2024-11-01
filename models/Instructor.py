from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder
import os
import base64

class Instructor():  
    def __init__(self, id=None, nombre=None, idioma_id = None ):
        self.id = id, 
        self.nombre = nombre, 
        self.nombre_id = idioma_id
        
    def catalogo(self, idiomaID, instructorID, disponibilidadID, fecha): 
        
        con = db().open
        cursor = con.cursor()
        
        sql = """ 
            SELECT 
                i.nombre, idi.nombre, dis.fecha, dis.hora_inicio, dis.hora_fin
            FROM 
                instructores as i 
                INNER JOIN idiomas as idi on (i.idioma_id=idi.id)
                INNER JOIN disponibilidad_instructores dis on (i.id = dis.instructor_id)
            WHERE
                idi.id = %s
                AND (case when %s = 0 then TRUE ELSE i.id = %s end)
                AND (case when %s = 0 then TRUE ELSE dis.id = %s end)
                AND (case when %s IS NULL then TRUE ELSE dis.fecha = %s end)
            ORDER BY 
                i.id
        
        """
        try: 
            #ejecutrar 
            cursor.execute(sql, [idiomaID, instructorID, instructorID, disponibilidadID, disponibilidadID, fecha, fecha])
            
            datos= cursor.fetchall()
            
            #convertir la hora_inicio y hora_fin en String 
            for i in range(len(datos)):
                datos[i]['hora_inicio'] = str(datos[i]['hora_inicio'])
                datos[i]['hora_fin'] = str(datos[i]['hora_fin'])
                
            
            #Retornar un mensaje con los datos de los productos
            if datos:
                return json.dumps({'status': True, 'data': datos, 'message': "Catálogo de instructores"}, cls=CustomJsonEncoder)
            else:
                return json.dumps({'status': True, 'data': None, 'message': "Sin registros"})
            
            
            
        except con.Error as error: 
            #Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
        
        