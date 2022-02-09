#!/usr/bin/env python3
from flask import Flask, request
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
import time
from config import PROFILE_PATH
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

# import for Email
import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

load_dotenv()

# Integration With SendPulse

# TODO: When you have your own Client ID and secret, put down their values here:
clientId = os.getenv('SENDPULSE_CLIENT_ID')
clientSecret = os.getenv('SENDPULSE_CLIENT_SECRET')
repoId = os.getenv('REPO_NUMBER_ID')
sendToEmail = os.getenv('SEND_TO_EMAIL')
fromToEmail = os.getenv('FROM_TO_EMAIL')
fromToPass = os.getenv('FROM_TO_PASS')

# GROUP CHATS
GRUPO_BOLETOS_AEREOS = "Solicitudes Instagram"
GRUPO_SEGUROS = "Solicitudes Instagram"
GRUPO_PAQUETES_TURISTICOS = "Solic. Internas VH PLUS"

# Method to take screenshot and send email
def screenShotAndSendEmail(imgName: str):

    driver.get_screenshot_as_file(imgName)

    msg = MIMEMultipart()
    msg['From'] = fromToEmail
    msg['To'] = sendToEmail
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "SS from Repochatbot"

    print(f"Credentials:\n From: {msg['From']} \n To: {msg['To']} \n Pass: {fromToPass}")

    msg.attach(MIMEText("Screenshot from Repochatbot"))
    with open(imgName, "rb") as img:
        part = MIMEApplication(
                img.read(),
                Name=basename(imgName)
                )

    #After the file is closed
    part['Content-Disposition'] = f'attachment; filename={basename(imgName)}'
    msg.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(fromToEmail, fromToPass)
        server.sendmail( fromToEmail, sendToEmail, msg.as_string() )


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

sem = threading.Semaphore()
lastGroupName = ""
print("Profile Path")
print(PROFILE_PATH)

print("Loading Firefox Webdirver")
options = Options()
options.headless = True
# options.add_argument("-profile")
# options.add_argument("/home/reponic/.mozilla/firefox/wsp.chatbot")
driver = webdriver.Firefox(options=options, executable_path=f'/home/{os.getlogin()}/Repochatbot/repochatbot-viajes-humboldt/geckodriver')

print("Getting Whatsapp Website")
driver.get("https://web.whatsapp.com")

print("Waiting for QR to show...")

try: 
    qr_element = WebDriverWait(driver,50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div')))

except:

    print("Taking Screenshot")
    screenShotAndSendEmail("wa_screenshot.png")

res = input("Input ss enter to take screenshot or press ENTER to continue...")
if res == "ss":
    res2 = ""
    while res2 == "":
        screenShotAndSendEmail("wa_screenshot.png")
        res2 = input("Input continue to continue or ENTER to keep taking screenshot...")

print("Start making requests!")
screenShotAndSendEmail(f"wa_screenshot_after_qr.png")

@application.route('/start_whatsapp_web', methods=['POST'])
def start_whatsapp_web():

    # Start the WebDriver and Login (If cache not set)
    return("success", 200)

@application.route('/screenshot', methods=['GET'])
def screenshot():

    print("Taking screenshot")
    screenShotandSendEmail("current_wa_state.png")
    return("success", 200)

@application.route('/repochatbot_api', methods=['POST'])
def repochatbot_api():

    sem.acquire()
    groupName = 'Bot API Viajes Humboldt'  # FIXME
    message = "Error"  # FIXME

    print("Entro en la funcion repochatbot")

    incoming_mesg = request.json
    if request.method == 'POST':
        print(f"Informacion Recibida:\n {incoming_mesg}")
    
    nombre = incoming_mesg['Nombre']
    telefono = incoming_mesg['Telefono']
    partida_destino = incoming_mesg['PartidaDestino']
        
    tipo_de_servicio = incoming_mesg['TipoDeServicio']

    message = f"Nuevo Cliente a la espera:\n*Nombre:* {nombre}\n*Telefono:* {telefono}\n*Partida - Destino:* {partida_destino}\n*Tipo de Servicio:* {tipo_de_servicio}\n"

    if tipo_de_servicio == "Boletos Aéreos":
        fecha_de_viaje = incoming_mesg['FechaViaje']
        pasajeros_cantidad = incoming_mesg['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\n*Cantidad de Pasajeros:* {pasajeros_cantidad}"

        groupName = GRUPO_BOLETOS_AEREOS

    elif tipo_de_servicio == "Paquetes Turísticos":
        fecha_de_viaje = incoming_mesg['FechaViaje']
        pasajeros_cantidad = incoming_mesg['PasajerosCantidad']

        message = message + f"*Fecha de Viaje:* {fecha_de_viaje}\n*Cantidad de Pasajeros:* {pasajeros_cantidad}"
        groupName = GRUPO_PAQUETES_TURISTICOS

    elif tipo_de_servicio == "Seguros De Viaje":
        cantidad_dias = incoming_mesg['DiasCantidad']
        edad = incoming_mesg['Edad']

        message = message + f"*Cantidad de Días:* {cantidad_dias}\n*Edad:* {edad}"
        groupName = GRUPO_SEGUROS

    if incoming_mesg['NoAtendido'] == "True":
        message = "*URGENTE!! NO HA SIDO ATENDIDO EN 2 HORAS:*\n\n" + message

    try:
        detalles_extras = incoming_mesg['DetallesExtra']
    except KeyError:
        print("No hay deatlles extras")

    message = f"{message} \n*Detalles Extras:* {detalles_extras} \n \n Grupo: {groupName}"

    try:
        if request.args.get('sendmessage') == "True":

            # ------- SENDPULSE MESSAGE -----------

            body_token = {
                'grant_type' : "client_credentials",
                'client_id' : clientId,
                'client_secret' : clientSecret
            }

            token_response = r = requests.post("https://api.sendpulse.com/oauth/access_token",
                    json=body_token)

            token_response = token_response.text

            token = json.loads(token_response)

            token = token['token_type'] + token['access_token']

            headers = {
                'accept': "application/json", 
                'Authorization': token,
                "Content-Type": "application/json"
            }

            jsonBody = {
                "contact_id": repoId,
                "message": {
                    "type": "text",
                    "text": {
                    "body": message
                    }
                }
            }

            try:
                r = requests.post("https://api.sendpulse.com/whatsapp/contacts/send", 
                    headers=headers,
                    json=jsonBody)
            except Exception as e:
                print("Algo ha pasado:\n {e}")

            print("Status code: " + str(r.status_code))
            print("RESPONSE : " + str(r.content))
    except e:
        print(e)

    # JUST FOR TESTING
    try:
        if request.args.get('test') == "True":
            groupName = "TestBot"
    except e:
        print(e)

    print("Enviando Mensaje")

    global lastGroupName

    if groupName != lastGroupName:
        lastGroupName = groupName
        Text_Box_Search = "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text"
        input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_css_selector(Text_Box_Search))
        input_box_search.click()
        input_box_search.clear()
        input_box_search.send_keys(groupName)
        selected_contact = driver.find_elements_by_xpath(f'.//span[@title = "{groupName}"]')
        selected_contact[0].click()

    inp_selector_chat = '#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div.p3_M1 > div > div._13NKt.copyable-text.selectable-text'
    input_box = driver.find_element_by_css_selector(inp_selector_chat)
    time.sleep(2)

    messages=message.split('\n')
    for msg in messages:
        input_box.send_keys(msg)
        input_box.send_keys(Keys.SHIFT,'\n')
    input_box.send_keys("\n")

    print("Mensaje Enviado")

    sem.release()

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
    
    application.run(use_reloader=False, use_evalex=False)
