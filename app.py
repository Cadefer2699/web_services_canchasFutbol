from flask import Flask

#Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.instructor import ws_instructor
from ws.reserva import ws_reserva

#Crear la variable de aplicación con Flask
app = Flask(__name__)


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)

app.register_blueprint(ws_instructor)
app.register_blueprint(ws_reserva)

@app.route('/')
def home():
    return 'Servicios web en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
