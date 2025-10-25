import os
import speech_recognition as sr
from elevenlabs import ElevenLabs
import matplotlib.pyplot as plt
import numpy as np
import pygame
import math

# Configurar la API de ElevenLabs
client = ElevenLabs(api_key="sk_d123150c074a8dabb93ba492395efdb9bf695f041fffd193")

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

#Función simulación
def simulacion_parabola():
    # Simulación de la parábola
    def draw_input_box(surface, text, x, y, active):
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(x, y, 200, 40)
        color = (255, 0, 0) if active else (100, 100, 100)
        pygame.draw.rect(surface, color, input_box, 2)
        text_surface = font.render(text, True, (255, 255, 255))
        surface.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        return input_box

    # Inicializar Pygame
    pygame.init()
    width, height = 1200, 750
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simulación de Semiparábola en el Aire")

    # Colores
    DARK_GRAY = (30, 30, 30)
    LIGHT_GRAY = (200, 200, 200)
    BLUE = (50, 150, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_BLUE = (0, 0, 139)
    BUTTON_COLOR = (70, 130, 180)
    BUTTON_HOVER_COLOR = (100, 150, 200)

    # Variables iniciales
    h0 = 300  # Altura inicial
    g = 9.81   # Gravedad
    results = ''  # Variable para mostrar resultados

    # Bucle principal
    running = True
    input_v0 = ''
    input_theta = ''
    active_v0 = False
    active_theta = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if active_v0:
                    if event.key == pygame.K_RETURN:
                        active_v0 = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_v0 = input_v0[:-1]
                    else:
                        input_v0 += event.unicode
                if active_theta:
                    if event.key == pygame.K_RETURN:
                        active_theta = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_theta = input_theta[:-1]
                    else:
                        input_theta += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Si se hace clic izquierdo
                    if v0_box.collidepoint(event.pos):
                        active_v0 = True
                        active_theta = False
                    elif theta_box.collidepoint(event.pos):
                        active_theta = True
                        active_v0 = False
                    else:
                        active_v0 = False
                        active_theta = False

        # Dibujar fondo y elementos
        screen.fill(DARK_GRAY)

        # Título
        font = pygame.font.Font(None, 48)
        title_surface = font.render(
            "Simulación de Semiparábola", True, LIGHT_GRAY)
        screen.blit(title_surface, (350, 20))

        # Instrucciones
        instruction_surface = font.render(
            "Ingrese Velocidad Inicial (m/s) y Ángulo (grados):", True, LIGHT_GRAY)
        screen.blit(instruction_surface, (200, 80))

        # Cuadros de entrada
        v0_box = draw_input_box(screen, input_v0, 480, 150, active_v0)
        theta_box = draw_input_box(screen, input_theta, 480, 220, active_theta)

        # Botón de inicio
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button = pygame.Rect(400, 400, 350, 50)
        if button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button)
        button_text = font.render("Iniciar Simulación", True, LIGHT_GRAY)
        screen.blit(button_text, (button.x + 30, button.y + 10))

        # Lógica de simulación
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                try:
                    v0 = float(input_v0)
                    theta = float(input_theta)
                    theta_rad = math.radians(theta)
                    time = 0
                    running_simulation = True
                    trajectory = []
                    x_values = []
                    y_values = []

                    # Bucle de la simulación
                    while running_simulation:
                        for sim_event in pygame.event.get():
                            if sim_event.type == pygame.QUIT:
                                running_simulation = False

                        # Lógica de movimiento
                        time += 0.1  # Incrementar tiempo en 0.1 segundos
                        x_position = v0 * math.cos(theta_rad) * time
                        y_position = h0 + (v0 * math.sin(theta_rad)
                                           * time) - (0.5 * g * (time ** 2))

                        # Detener la simulación cuando el proyectil toca el suelo
                        if y_position <= 0:
                            running_simulation = False
                            y_position = 0  # Asegurarse de que y_position no sea negativa

                        # Almacenar las posiciones para el gráfico
                        x_values.append(x_position)
                        y_values.append(y_position)

                        # Limpiar la pantalla
                        screen.fill(DARK_GRAY)

                        # Dibujar proyectil
                        if y_position >= 0:  # Solo dibujar si el proyectil está en el aire
                            pygame.draw.circle(
                                screen, BLUE, (int(x_position), int(height - y_position)), 10)
                            # Almacenar trayectoria
                            trajectory.append(
                                (int(x_position), int(height - y_position)))

                        # Dibujar la trayectoria
                        if len(trajectory) > 1:
                            # Dibujar la línea de trayectoria
                            pygame.draw.lines(
                                screen, RED, False, trajectory, 2)

                        # Mostrar resultados en pantalla
                        results = f"Tiempo total de vuelo: {time:.2f} s | Distancia horizontal: {x_position:.2f} píxeles | Altura máxima: {max(y_values):.2f} píxeles"
                        result_surface = font.render(results, True, LIGHT_GRAY)
                        screen.blit(result_surface, (50, 680))

                        pygame.display.flip()
                        # Esperar un tiempo antes del siguiente frame
                        pygame.time.delay(100)

                    # Análisis del movimiento
                    total_time = time
                    horizontal_distance = x_position
                    max_height = max(y_values)

                    # Mostrar resultados en consola
                    print(f"Tiempo total de vuelo: {total_time:.2f} segundos")
                    print(f"Distancia horizontal recorrida: {horizontal_distance:.2f} píxeles")
                    print(f"Altura máxima alcanzada: {max_height:.2f} píxeles")

                    # Graficar posiciones
                    plt.figure(figsize=(10, 5))

                    # Gráfico de trayectoria
                    plt.subplot(1, 2, 1)
                    plt.plot(x_values, y_values, color='blue')
                    plt.title('Trayectoria del Proyectil')
                    plt.xlabel('Distancia Horizontal (píxeles)')
                    plt.ylabel('Altura (píxeles)')
                    plt.grid()

                    # Gráfico de tiempo vs posición
                    plt.subplot(1, 2, 2)
                    time_values = [i * 0.1 for i in range(len(x_values))]
                    plt.plot(time_values, x_values,
                             label='Posición Horizontal', color='orange')
                    plt.plot(time_values, y_values,
                             label='Altura', color='green')
                    plt.title('Movimiento del Proyectil')
                    plt.xlabel('Tiempo (s)')
                    plt.ylabel('Posición (píxeles)')
                    plt.legend()
                    plt.grid()

                    plt.tight_layout()
                    plt.show()

                except ValueError:
                    print(
                        "Por favor, ingrese valores válidos para la velocidad y el ángulo.")
        # Cerrar Pygame
        pygame.display.flip()
    pygame.quit()

#Funcion para que salude
def mensaje_bienvenida():
    """Envía un mensaje de bienvenida al usuario."""
    saludo = "¡Hola! Soy Neocolmet, mucho gusto. Estoy aquí para ayudarte con temas de física, simulaciones y otros temas que podrían interesarte. ¿Por dónde quieres empezar?"
    respuesta_hablada(saludo)

# Función para preguntar sobre un tema de física
def clase_de_fisica():
    """Pregunta al usuario sobre un tema de física y proporciona una definición breve."""
    pregunta = "¡Genial! hablemos un poco de física. ¿Sobre qué tema de física te gustaría hablar? Puedes mencionar temas como 'movimiento', 'fuerzas', 'energía', 'termodinámica', etc."
    respuesta_hablada(pregunta)
    
    tema = escuchar_comando()
    
    definiciones = {
        "movimiento": "El movimiento es el cambio de posición de un objeto con respecto a un sistema de referencia en un intervalo de tiempo .",
        "fuerzas": "Las fuerzas son interacciones que pueden cambiar el estado de movimiento de un objeto. Se miden en Newtons.",
        "energía": "La energía es la capacidad de realizar trabajo. Puede presentarse en diversas formas, como energía cinética, potencial, térmica, entre otras.",
        "termodinámica": "La termodinámica es la rama de la física que estudia las relaciones entre el calor, el trabajo y la energía.",
        "mecánica": "La mecánica es la rama de la física que estudia el movimiento de los objetos y las fuerzas que actúan sobre ellos.",
        "movimiento rectilíneo uniforme": "El movimiento rectilíneo uniforme es un tipo de movimiento en el que un objeto se mueve en una línea recta a una velocidad constante.",
        "movimiento circular uniforme": "El movimiento circular uniforme es un tipo de movimiento en el que un objeto se mueve en una trayectoria circular a una velocidad constante.",
        
    }
    
    if tema in definiciones:
        respuesta = definiciones[tema]
        respuesta_hablada(respuesta)
    elif tema == "movimiento parabólico":
        respuesta = "El movimiento parabólico es un tipo de movimiento en el que un objeto se mueve en una trayectoria parabólica bajo la influencia de la gravedad. Tengo una simulación que podría ayudarte a entender mejor este concepto."
        respuesta_hablada(respuesta)
        simulacion_parabola()

    else:
        respuesta_hablada("Lo siento, no tengo información sobre ese tema. Por favor, elige otro.")

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

# Mapeo de comandos a funciones
def ejecutar_comando(comando):
    if "clase de física" in comando:
        clase_de_fisica()

    elif "iniciar simulación" in comando:
        texto = "¡Genial! Estoy listo para empezar la simulación. ¿Qué tipo de simulación deseas realizar? Puedes elegir entre 'simulación de parábola' o 'simulación de movimiento circular'. Prueba diciendo alguno de estos."
        respuesta_hablada(texto)

    elif "simulación de parábola" in comando:
        texto = "Iniciando simulación de la parábola"
        respuesta_hablada(texto)
        simulacion_parabola()
        texto2 = """Simulación finalizada. Esta simulación, desarrollada por Santiago Cervantes para contribuir en mis funcionalidades, representa el movimiento parabólico, una clase de física que, en nuestro colegio, fue dada por el profe Jesús García. El movimiento parabólico es un tipo de movimiento que sigue una trayectoria en forma de parábola. Ocurre cuando un objeto es lanzado hacia arriba y al frente, bajo la influencia de la gravedad, y su desplazamiento se descompone en dos componentes. ¿En qué más puedo ayudarte?"""
        respuesta_hablada(texto2)
    else:
        respuesta_hablada("Lo siento, no entendí el comando. Por favor, repite.")

# Bucle principal
def main():
    mensaje_bienvenida()
    while True:
        comando = escuchar_comando()
        if comando:
            if "salir" in comando:
                respuesta_hablada("Hasta luego. Gracias por usar NeoColmet.")
                break
            ejecutar_comando(comando)

if __name__ == "__main__":
    main()