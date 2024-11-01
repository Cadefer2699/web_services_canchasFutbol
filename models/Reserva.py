from conexionBD import Conexion as db
import json

class Reserva(): 
    def __init__(self,id = None, estudiante_id = None, metodo_pago = None, instructor_id = None, idioma_id = None, disponibilidad_id = None, detalle_reserva = None):
        self.id = id
        self.estudiante_id = estudiante_id
        self.metodo_pago = metodo_pago
        self.instructor_id = instructor_id
        self.idioma_id = idioma_id
        self.disponibilidad_id = disponibilidad_id
        self.detalle_reserva = detalle_reserva
        
    
    def insertar(self): 
        con = db().open
        cursor = con.cursor()
        
        try: 
            con.autocommit = False #Indica que la transacción se verificará y confirmará de manera manual
            
            #insertar la reserva
            sql = """INSERT INTO reserva (estudiante_id, metodo_pago) VALUES (%s, %s)"""
            cursor.execute(sql, [self.estudiante_id, self.metodo_pago])
            
            #obtener el id de la reserva
            self.id = con.insert_id()
            
            #insertar en detalle_reserva
            sql_insertar_detalle_reserva = "insert into detalle_reserva (reserva_id, instructor_id, idioma, fecha, hora_inicio, hora_fin, tipo_clase) values (%s, %s, %s, %s, %s, %s, %s)"
            
            detalleReservaJSONObjectArray = json.loads(self.detalle_reserva)
            
            #recorrer el JSON Array 
            for reserva in detalleReservaJSONObjectArray:
                instructor_id = reserva('instructor_id')
                idioma = reserva('idioma')
                fecha = reserva('fecha')
                hora_inicio = reserva('hora_inicio')
                hora_fin = reserva('hora_fin')
                tipo_clase = reserva('tipo_clase')
                
                
                cursor.execute(sql_insertar_detalle_reserva, [self.id, instructor_id, idioma, fecha, hora_inicio, hora_fin, tipo_clase])
                
            #confirmar la transacción
            con.commit()
            
            #retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Reserva insertada correctamente'}) 
        
            
        except con.Error as error:
            con.rollback()
            return json.dumps({'status':False, 'data':None, 'message':str(error)})
        
        finally: 
            cursor.close()
            con.close()