from conexionBD import Conexion as db
import json

class Sesion():
    def __init__(self, email=None, clave=None):
        self.email = email
        self.clave = clave

    def iniciarSesion(self):
        #Abrir la conexión a la BD
        con = db().open

        try:
            #Crear un cursor para almacenar los datos que devuelve la consuñta SQL, al validar las credenciales del usuario
            cursor = con.cursor()

            #Preparar una consulta SQL select para validar las credenciales del usuario
            sql = """
                    SELECT
                        u.id,
                        u.nombre,
                        u.email,
                        u.estado_usuario,
                        u.almacen_id,
                        CONCAT('/static/imgs-usuario/', u.img) as foto
                    FROM
                        usuario u
                    WHERE
                        email = %s
                        and clave = %s;
                """
            
            #Ejecutar la consulta SQL
            cursor.execute(sql, [self.email, self.clave])

            #Almancenar el resultado de la consulta SQL ejecutada
            datos = cursor.fetchone()

            #Retonar el resultado
            if datos: #Validar si la consulta sql ha devuelvo registros
                if datos['estado_usuario'] == '1': #1:Activo; 0:Inactivo
                    return json.dumps({'status': True, 'data': datos, 'message': 'Inicio de sesión satisfactorio. Bienvenido a la aplicación'})
                else: #El usuario se encuentra inactivo
                    return json.dumps({'status': False, 'data': None, 'message': 'Cuenta inactiva. Consulte al administrador'})
            else: #No hay datos
                return json.dumps({'status': False, 'data': None, 'message': 'Credenciales incorrectas, por favor verifique'})

        except con.Error as error:
            #Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

    def actualizarToken(self, token, UsuarioID):
        #Abrir conexión a la base de datos
        con = db().open

        #Crear un cursor para almacenar los datos que devuelve la consulta SQL
        cursor = con.cursor()

        #Preparar una sentencia que permita actualizar el token del usuario en la BD
        sql = "update usuario set token=%s, estado_token='1' where id = %s"
        
        #Iniciar con la actualización del token
        try:
            #Configurar la transacción
            con.autocommit = False #Indica que la transacción se verificará y confirmará de manera manual

            #Ejecutar la sentencia
            cursor.execute(sql, [token, UsuarioID])

            #Ejecutar la sentencia #2
            #cursor.execute(sql2, [par1, par2])

            #Ejecutar la sentencia #3
            #cursor.execute(sql3, [parx, pary])

            #Confirmar la sentencia de actualización
            con.commit() #Confirma la transacción

        except con.Error as error:
            #Revocar la actualización
            con.rollback()

            #Retonar un mensaje
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

        #Si todo el método se ha ejecutado correctamente, entonces devuelvo un mensaje con TRUE
        return json.dumps({'status': True, 'data': None, 'message': "Token actualizado correctamente"})

    def validarEstadoToken(self, usuarioID):
        #Abrir una conexión a la BD
        con = db().open

        #Crear un cursor para almacenar los datos que devuelve la consulta SQL
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "select estado_token from usuario where id=%s"
        
        #Ejecutar la consulta SQL
        cursor.execute(sql, [usuarioID])

        #Almacenar los datos que devuelve la consulta SQL
        datos = cursor.fetchone()

        #Cerrar el cursor y la conexión a la BD
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status':True, 'data':datos, 'message':'Estado de token'})
        else:
            return json.dumps({'status':False, 'data':None, 'message':'Estado de token no encontrado'})
