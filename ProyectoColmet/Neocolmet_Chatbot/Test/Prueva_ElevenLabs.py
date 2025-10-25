import pygame
from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="sk_d123150c074a8dabb93ba492395efdb9bf695f041fffd193")

# Generar el audio
audio = client.generate(
    text="Hola a todos, soy un modelo de lenguaje generado por ElevenLabs y configurado por santi para generar audio, que, proximamente, será utilizado en un proyecto de IA",
    voice="Brian",
    model="eleven_multilingual_v2"
)

# Convertir el generador en datos binarios y guardarlo en un archivo
with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

# Inicializar pygame para reproducir el audio
pygame.mixer.init()
pygame.mixer.music.load("output.mp3")
pygame.mixer.music.play()

# Espera a que termine la reproducción
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

