#!/usr/bin/env python3
from flask import Flask, request
import requests
import json

# Integration With SendPulse

# TODO: When you have your own Client ID and secret, put down their values here:
clientId = "101800f95cbe9e47fa8fbe68685be3c2"
clientSecret = "f9694fb799bcb4657a740433b9083a81"

repo_id = "61d83bcc256dd967f942d71c"

# GROUP CHATS
GRUPO_BOLETOS_AEREOS = "Solicitudes Instagram"
GRUPO_SEGUROS = "Solicitudes Instagram"
GRUPO_PAQUETES_TURISTICOS = "Solic. Internas VH PLUS"


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>RepoChatBot</title> </head>\n<body>'''
instructions = '''
    <p><em>RepoChatBot</em>: This is a RESTful web service for the RepoChatBot!</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text + instructions + footer_text))

@application.route('/repochatbot_api', methods=['POST'])
def repochatbot_api():
    groupName = 'Bot API Viajes Humboldt'  # FIXME
    message = "Error"  # FIXME

    print("Entro en la funcion repochatbot")

    incoming_mesg = request.json
    if request.method == 'POST':
        print(f"Informacion Recibida:\n {incoming_mesg}")
    
    nombre = incoming_mesg['Nombre']
    telefono = incoming_mesg['Telefono']
    partida_destino = incoming_mesg['PartidaDestino']
    try:
        detalles_extras = incoming_mesg['DetallesExtra']
    except KeyError:
        print("No hay deatlles extras")
        
    tipo_de_servicio = incoming_mesg['TipoDeServicio']

    message = f"Nuevo Cliente a la espera:\n*Nombre:* {nombre}\n*Telefono:* {telefono}\n*Partida - Destino:* {partida_destino}\n*Tipo de Servicio:* {tipo_de_servicio}\n"

    if tipo_de_servicio == "Boletos Aéreos":
        fecha_de_viaje = incoming_mesg['FechaViaje']
        pasajeros_cantidad = incoming_mesg['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\nCantidad de Pasajeros: {pasajeros_cantidad}"

        groupName = GRUPO_BOLETOS_AEREOS

    elif tipo_de_servicio == "Paquetes Turísticos":
        fecha_de_viaje = incoming_mesg['FechaViaje']
        pasajeros_cantidad = incoming_mesg['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\nCantidad de Pasajeros: {pasajeros_cantidad}"
        groupName = GRUPO_PAQUETES_TURISTICOS

    elif tipo_de_servicio == "Seguros De Viaje":
        cantidad_dias = incoming_mesg['DiasCantidad']
        edad = incoming_mesg['Edad']

        message = message + f"*Cantidad de Días:* {cantidad_dias}\nEdad: {edad}"
        groupName = GRUPO_SEGUROS

        if incoming_mesg['NoAtendido'] == "True":
            message = "URGENTE!! NO HA SIDO ATENDIDO EN 2 HORAS:\n\n" + message

    body_token = {
        'grant_type' : "client_credentials",
        'client_id' : '101800f95cbe9e47fa8fbe68685be3c2',
        'client_secret' : 'f9694fb799bcb4657a740433b9083a81'
    }

    token_response = r = requests.post("https://api.sendpulse.com/oauth/access_token",
            json=body_token)

    token_response = token_response.text

    token = json.loads(token_response)

    token = token['token_type'] + token['access_token']

    message = f"{message} \n \n Grupo: {groupName}"

    headers = {
    'accept': "application/json", 
    'Authorization': token,
    "Content-Type": "application/json"
    }

    jsonBody = {
    "contact_id": "61d83bcc256dd967f942d71c",
    "message": {
        "type": "text",
        "text": {
        "body": message
        }
  }
    }

    print("Enviando Mensaje")

    try:
        r = requests.post("https://api.sendpulse.com/whatsapp/contacts/send", 
            headers=headers,
            json=jsonBody)
    except Exception as e:
        print("Algo ha pasado:\n {e}")


    print("Status code: " + str(r.status_code))
    print("RESPONSE : " + str(r.content))

    return("success", 200)

# Flask Implementation
@application.route('/repochatbot', methods=['POST'])
def repochatbot():
    
    groupName = 'Bot API Viajes Humboldt'  # FIXME
    message = "Error"  # FIXME

    print("Entro en la funcion repochatbot")

    incoming_mesg = request.json
    if request.method == 'POST':
        print(f"Informacion Recibida:\n {incoming_mesg}")
    
    nombre = incoming_mesg[0]['contact']['variables']['Nombre']
    telefono = incoming_mesg[0]['contact']['variables']['Telefono']
    partida_destino = incoming_mesg[0]['contact']['variables']['Partida_Destino']
    try:
        detalles_extras = incoming_mesg[0]['contact']['variables']['DetallesExtra']
    except KeyError:
        print("No hay deatlles extras")
        
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

    body_token = {
        'grant_type' : "client_credentials",
        'client_id' : '101800f95cbe9e47fa8fbe68685be3c2',
        'client_secret' : 'f9694fb799bcb4657a740433b9083a81'
    }

    token_response = r = requests.post("https://api.sendpulse.com/oauth/access_token",
            json=body_token)

    token_response = token_response.text

    token = json.loads(token_response)

    token = token['token_type'] + token['access_token']

    message = f"{message} \n \n Grupo: {groupName}"

    headers = {
    'accept': "application/json", 
    'Authorization': token,
    "Content-Type": "application/json"
    }

    jsonBody = {
    "contact_id": "61d83bcc256dd967f942d71c",
    "message": {
        "type": "text",
        "text": {
        "body": message
        }
  }
    }

    print("Enviando Mensaje")

    try:
        r = requests.post("https://api.sendpulse.com/whatsapp/contacts/send", 
            headers=headers,
            json=jsonBody)
    except Exception as e:
        print("Algo ha pasado:\n {e}")


    print("Status code: " + str(r.status_code))
    print("RESPONSE : " + str(r.content))

    return("success", 200)

if __name__ == '__main__':
    
    application.run(debug=True)