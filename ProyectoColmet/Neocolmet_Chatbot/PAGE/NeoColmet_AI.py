import os
import speech_recognition as sr
from elevenlabs import ElevenLabs
import matplotlib.pyplot as plt
import numpy as np
import pygame
import math
import google.generativeai as genai
import textwrap
from IPython.display import Markdown
import sys
sys.stdout.reconfigure(encoding="utf-8")

#Configurar API de Gemini
modelo = genai.GenerativeModel("gemini-2.5-flash")

GOOGLE_API_KEY = "AIzaSyBOv0gSRO2iR2S_XOE3k_JFhry0hcEkFKM"
genai.configure(api_key=GOOGLE_API_KEY)

def rebajar(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, ">", predicate=lambda _: True))

def limitar_palabras(texto, max_palabras):
    palabras = texto.split()
    if len(palabras) > max_palabras:
        return ' '.join(palabras[:max_palabras]) + '...'
    return texto

# Configurar la API de ElevenLabs
client = ElevenLabs(api_key="sk_4b71d49009158e6d804d480c2f226fc6c293c16d0baeaa0f")

# Inicializar Pygame
pygame.init()

# Función para generar y reproducir respuesta hablada
def respuesta_hablada(texto):
    """Genera y reproduce respuesta hablada usando ElevenLabs y Pygame."""
    audio_generator = client.generate(text=texto, voice="George", model="eleven_multilingual_v1")
    audio_bytes = b"".join(audio_generator)
    reproducir_audio(audio_bytes)

# Función para reproducir audio
def reproducir_audio(audio_bytes):
    """Reproduce audio MP3 usando Pygame."""
    archivo_temporal = "audio_output.mp3"
    
    with open(archivo_temporal, "wb") as f:
        f.write(audio_bytes)
    
    pygame.mixer.init()
    pygame.mixer.music.load(archivo_temporal)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(archivo_temporal)


# Función para escuchar comandos de voz
def escuchar_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("No se entendió el comando.")
            return None
        except sr.WaitTimeoutError:
            print("No se detectó ninguna voz a tiempo.")
            return None


def mensaje_bienvenida():
    """Envía un mensaje de bienvenida al usuario."""
    saludo = "¡Hola! Soy Neocolmet, mucho gusto. ¿Por dónde quieres empezar?"
    respuesta_hablada(saludo)


# Bucle principal
def main():
    mensaje_bienvenida()
    while True:
        comando = escuchar_comando()
        if comando:
            respuesta = modelo.generate_content(comando)
            respuesta_limitada = limitar_palabras(respuesta.text, 50)  # Cambia 50 por el límite que desees
            print(f"Respuesta generada: {respuesta_limitada}")
            respuesta_hablada(respuesta_limitada)

        if "salir" in comando:
            respuesta_hablada("Hasta luego. Gracias por usar NeoColmet.")
            break

if __name__ == "__main__":
    main()