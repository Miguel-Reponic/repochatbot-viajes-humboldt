import requests
import json
import time
import argparse

base_local_request = "http://127.0.0.1:5000/"
endpoint_message = "repochatbot_api?test=True"

external_request = ""

parser = argparse.ArgumentParser()
parser.add_argument("-ss", "--ScreenShot", default=False, help="Make Screenshot request")

webhook_url = base_local_request
args = parser.parse_args()
try:
    ss = args.ScreenShot
    print(f"Take Screenshot: {ss}")
except:
    ss = False



data = [
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
         "username":"Viajes Humboldt",
         "name":"Viajes Humboldt",
         "tags":[
            
         ],
         "last_message":"no",
         "photo":"None",
         "variables":{
            "FechaDeViaje":"11/11/2012 00:00:00",
            "Fecha_Viaje":"12/12/2021",
            "PasajerosCantidad":8,
            "Partida_Destino":"caracas, miami",
            "DetallesExtra":"no",
            "Nombre":"gabriela Diaz",
            "Telefono":"+584122614445",
            "NoAtendido":"False"
         },
         "phone":"584122614445",
         "id":"619b9a2965c4657d996c56f1"
      },
      "date":1638797555
   }
]

prueba_1 = {
"Nombre" : "Reponic T",
"Telefono" : "+5554442233",
"PartidaDestino" : "Caracas",
"FechaViaje" : "02/28/2022",
"PasajerosCantidad" : "2",
"DetallesExtra" : "ESTO ES UNA PRUEBA",
"TipoDeServicio" : "Boletos Aéreos",
"NoAtendido": "False"
}

prueba_2 = {
"Nombre" : "Reponic T",
"Telefono" : "+5554442233",
"PartidaDestino" : "Caracas",
"FechaViaje" : "02/28/2022",
"PasajerosCantidad" : "2",
"DetallesExtra" : "ESTO ES UNA PRUEBA",
"TipoDeServicio" : "Boletos Aéreos",
"NoAtendido": "True"
}

prueba_3 = {
"Nombre" : "Reponic T",
"Telefono" : "+5554442233",
"PartidaDestino" : "Caracas",
"FechaViaje" : "02/28/2022",
"PasajerosCantidad" : "2",
"DetallesExtra" : "ESTO ES UNA PRUEBA",
"TipoDeServicio" : "Boletos Aéreos",
"NoAtendido": "True"
}


if ss == "True":

    r = requests.get(webhook_url+"/screenshot")
    print("Request result: ")
    print(r)

else:
    print("Prueba 1")
    print(prueba_1)
    r = requests.post(webhook_url+endpoint_message, data=json.dumps(prueba_1), headers={'Content-Type': 'application/json'})
    time.sleep(1)
    print("Prueba 2")
    print(prueba_2)
    r = requests.post(webhook_url+endpoint_message, data=json.dumps(prueba_2), headers={'Content-Type': 'application/json'})
    time.sleep(1)
    print("Prueba 3")
    print(prueba_3)
    r = requests.post(webhook_url+endpoint_message, data=json.dumps(prueba_3), headers={'Content-Type': 'application/json'})
