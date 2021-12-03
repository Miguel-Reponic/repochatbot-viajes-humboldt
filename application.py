#!/usr/bin/env python3
from flask import Flask, request
import requests


# GROUP CHATS
GRUPO_BOLETOS_AEREOS = "Solicitudes Instagram"
GRUPO_SEGUROS = "Solicitudes Instagram"
GRUPO_PAQUETES_TURISTICOS = "Solic. Internas VH PLUS"

# TODO: When you have your own Client ID and secret, put down their values here:
instanceId = "33"
clientId = "miguel.tannous@reponic.org"
clientSecret = "464d0e47ae24491c94646c0a6ae2b4b9"

# TODO: Customize the following 3 lines
groupName = 'Bot API Viajes Humboldt'  # FIXME
groupAdmin = "14079708692"  # FIXME
message = "Error"  # FIXME


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>RepoChatBot</title> </head>\n<body>'''
instructions = '''
    <p><em>RepoChatBot</em>: This is a RESTful web service for the RepoChatBot!</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

application = Flask(__name__)

headers = {
    'X-WM-CLIENT-ID': clientId, 
    'X-WM-CLIENT-SECRET': clientSecret
}

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text + instructions + footer_text))

# Flask Implementation
@application.route('/repochatbot', methods=['POST'])
def repochatbot():

    """
    JSON FORMAT FROM SENDPULSE
    [
        {
            "info":"None",
            "service":"whatsapp",
            "title":"Boletos Aéreos",
            "bot":{
                "external_id":"584121628358",
                "id":"618c82750709bc6a90276a86",
                "name":"Viajes Humboldt Repochat"
            },
            "contact":{
                "username":"Reponic",
                "name":"Reponic",
                "tags":[
                    
                ],
                "last_message":"2",
                "photo":"None",
                "variables":{
                    "FechaDeViaje":"12/02/2022 00:00:00",
                    "Nombre":"Miguel Tannous",
                    "Telefono":"+581234567891",
                    "PasajerosCantidad":2,
                    "Partida_Destino":"Caracas, Venezuela - Miami, USA"
                },
                "phone":"14079708692",
                "id":"618ca0211fdcb2586a4f7eaf"
            },
            "date":1637207046
        }
    ]
    """

    incoming_mesg = request.json
    if request.method == 'POST':
        print(f"Información Recibida:\n {incoming_mesg}")
    
    nombre = incoming_mesg[0]['contact']['variables']['Nombre']
    telefono = incoming_mesg[0]['contact']['variables']['Telefono']
    partida_destino = incoming_mesg[0]['contact']['variables']['Partida_Destino']
    detalles_extras = incoming_mesg[0]['contact']['variables']['DetallesExtra']
    tipo_de_servicio = incoming_mesg[0]['title']

    message = f"Nuevo Cliente a la espera:\n*Nombre:* {nombre}\n*Telefono:* {telefono}\n*Partida - Destino:* {partida_destino}\n*Tipo de Servicio:* {tipo_de_servicio}\n"

    if tipo_de_servicio == "Boletos Aéreos":
        fecha_de_viaje = incoming_mesg[0]['contact']['variables']['FechaDeViaje']
        pasajeros_cantidad = incoming_mesg[0]['contact']['variables']['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\nCantidad de Pasajeros: {pasajeros_cantidad}"

        groupName = GRUPO_BOLETOS_AEREOS

    elif tipo_de_servicio == "Paquetes Turísticos":
        fecha_de_viaje = incoming_mesg[0]['contact']['variables']['FechaDeViaje']
        pasajeros_cantidad = incoming_mesg[0]['contact']['variables']['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\nCantidad de Pasajeros: {pasajeros_cantidad}"
        groupName = GRUPO_PAQUETES_TURISTICOS

    elif tipo_de_servicio == "Seguros De Viaje":
        cantidad_dias = incoming_mesg[0]['contact']['variables']['DiasCantidad']
        edad = incoming_mesg[0]['contact']['variables']['Edad']

        message = message + f"*Cantidad de Días:* {cantidad_dias}\nEdad: {edad}"
        groupName = GRUPO_SEGUROS

    if incoming_mesg[0]['contact']['variables']['DiasCantidad'] == "True":
        message = "URGENTE!! NO HA SIDO ATENDIDO EN 2 HORAS:\n\n" + message

    jsonBody = {
        'group_name': groupName,
        'group_admin': groupAdmin,
        'message': message
    }

    print("Enviando Mensaje")

    try:
        r = requests.post("http://api.whatsmate.net/v3/whatsapp/group/text/message/%s" % instanceId, 
            headers=headers,
            json=jsonBody)
    except Exception as e:
        print("Algo ha pasado:\n {e}")


    print("Status code: " + str(r.status_code))
    print("RESPONSE : " + str(r.content))

    return("success", 200)

if __name__ == '__main__':
    
    application.run(debug=True)