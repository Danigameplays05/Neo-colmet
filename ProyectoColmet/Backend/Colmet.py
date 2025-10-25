import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import pybible as pb
import os
import pyjokes
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import seaborn as sns
import tkinter as tk
from tkinter import messagebox
import pygame
import math
import threading
import os
import http.server
import socketserver
import threading
from contextlib import suppress
import customtkinter as ctk
import webbrowser
import atexit

#Configuración de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()
#nombre del asistente
nombre_asistente = "Colmet"

#almacenamos nuestro nombre
archivo_nombre = "nombre_usuario.txt"

def establecer_nombre_usuario():
    hablar= ("Hola, cómo estás?")

    with sr.Microphone() as source:
        #ajustamos el ruido ambiental
        recognizer.adjust_for_ambient_noise(source,duration=1)

        try:
            audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)

            nombre= recognizer.recognize_google(audio,language='en-CO')

            with open(archivo_nombre,'w') as file:
                
                file.write(nombre)

            return nombre.lower()
        
        except sr.WaitTimeoutError:
            return ""
        
        except sr.UnknownValueError:
            return ""


def obtener_hora_actual():
    hora = datetime.datetime.now()

    hora = hora.strftime('%H: %M: %S')

    return hora 

def obtener_saludo():

    hora = datetime.datetime.now()

    hora = hora.hour

    if 5<= hora < 12:
        return "¡Buenas tardes, cómo se están docentes y maestros?!, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel, alguien quien tenía este proyecto desde hace mucho tiempo, pero no había podido presentarlo. Originalmente, he surgido a causa de los avances tecnológicos que se han venido presentando, por lo cual Daniel pensó en crear un modelo de inteligencia artificial o asistente virtual, que pudiese automatizar tareas. Así que"
    elif 12 <= hora<18:
        return "¡buenas tardes, cómo están?!, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial diseñada para la asistencia académica de los estudiantes de la institución. "
    else:
        return "Buenas noches, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel"
#buscar conceptos, personas, significados etc.
def quien_es(person):
    try:
        info = wikipedia.summary(person, 1)
        hablar(f"Según Wikipedia, {person} es {info}")
        print(info)
    except wikipedia.exceptions.DisambiguationError as e:
        hablar(f"Lo siento, hay varias personas con el nombre de {person}. Puedes ser más específico?")
    except wikipedia.exceptions.PageError:
        hablar(f"Lo siento, no encontré información sobre {person} en Wikipedia.")

def definir_concepto(concepto):
    try:
        info = wikipedia.summary(concepto, sentences=2)  # Obtener un resumen de 2 oraciones
        hablar(f"Según Wikipedia, {concepto} es {info}")
        print(info)  # Imprimir la información en la consola
    except wikipedia.exceptions.DisambiguationError as e:
        hablar(f"Lo siento, hay varias definiciones para {concepto}. Puedes ser más específico?")
    except wikipedia.exceptions.PageError:
        hablar(f"Lo siento, no encontré información sobre {concepto} en Wikipedia.")
        

def subir_volumen():
    engine.setProperty('volume', engine.getProperty('volume') + 1)
    hablar("Volumen subido")

def bajar_volumen():
    engine.setProperty('volume', engine.getProperty('volume') - 1)
    hablar("Volumen bajado")


#buscar en la web
def buscar_en_google(busqueda):
    url = f"https://www.google.com/search?q={busqueda}"
    webbrowser.open(url)
# abrir redes y apps
def abrir_youtube():
    webbrowser.open('https://www.youtube.com')
def abrir_facebook():
    webbrowser.open('https://www.facebook.com')
def abrir_discord():
    webbrowser.open('https://discord.com')
def abrir_whatsapp():
    webbrowser.open('https://web.whatsapp.com')
def abrir_instagram():
    webbrowser.open('https://www.instagram.com')
def abrir_spotify():
    url = 'https://www.spotify.com'
    webbrowser.open(url)
def abrir_tiktok():
    webbrowser.open('https://www.tiktok.com')
def abrir_aplicacion(aplicacion):
    try:
        os.startfile(aplicacion)
        hablar(f"Abriendo {aplicacion}")
    except FileNotFoundError:
        hablar(f"Lo siento, no encontré la aplicación {aplicacion}")


# Crear historia con IA
def crear_historia():
    import random

    # Personajes
    personajes = ["Juan", "María", "Pedro", "Ana", "Luis"]

    # Lugares
    lugares = ["la playa", "el parque", "la montaña", "la ciudad", "el bosque"]

    # Objetos
    objetos = ["un libro", "una pelota", "un reloj", "un teléfono", "un bolígrafo"]

    # Acciones
    acciones = ["corrió", "saltó", "caminó", "nadó", "voló"]

    # Generar la historia
    historia = f"Había una vez un personaje llamado {random.choice(personajes)} que vivía en {random.choice(lugares)}. Un día, {random.choice(personajes)} encontró {random.choice(objetos)} y decidió {random.choice(acciones)} hacia {random.choice(lugares)}. En el camino, conoció a {random.choice(personajes)} y juntos decidieron {random.choice(acciones)} hacia {random.choice(lugares)}. Al final, {random.choice(personajes)} y {random.choice(personajes)} se convirtieron en grandes amigos y vivieron felices para siempre."

    return historia

def contar_historia():
    historia = crear_historia()
    hablar(historia)




#decir bromas
def contar_broma():
    joke = pyjokes.get_joke(language='es')
    hablar(joke)
    print(joke)



#búsqueda de versículos, y libros de la bilbia (aún se está trabajando)
def buscar_versiculo(libro, capitulo, versiculo, traduccion):
    if traduccion == 'RV1960':
        bible = pb.Bible('RV1960')
    elif traduccion == 'NTV':
        bible = pb.Bible('NTV')
    elif traduccion == 'NIV':
        bible = pb.Bible('NIV')
    elif traduccion == 'LBLA':
        bible = pb.Bible('LBLA')
    else:
        hablar("Lo siento, no tengo esa traducción disponible")
        return

    try:
        verse = bible.get_verse(libro, capitulo, versiculo)
        hablar(f"El versículo {versiculo} del capítulo {capitulo} del libro de {libro} dice: {verse}")
    except pb.VersicleNotFoundError:
        hablar(f"Lo siento, no encontré el versículo {versiculo} del capítulo {capitulo} del libro de {libro}")
def buscar_libro(libro, traduccion):
    if traduccion == 'RV1960':
        bible = pb.Bible('RV1960')
    elif traduccion == 'NTV':
        bible = pb.Bible('NTV')
    else:
        hablar("Lo siento, no tengo esa traducción disponible")
        return

    try:
        book = bible.get_book(libro)
        hablar(f"El libro de {libro} tiene {len(book)} capítulos")
    except pb.BookNotFoundError:
        hablar(f"Lo siento, no encontré el libro de {libro}")


#graficar funciones, mapas, cosas relacionadas a física
def graficar_funcion(funcion, rango):
    x = np.linspace(rango[0], rango[1], 100)
    y = eval(funcion)
    plt.plot(x, y)
    plt.title(f'Gráfico de {funcion}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.show()


def simular_movimiento(gravedad=9.81, tiempo=5):
    t = np.linspace(0, tiempo, num=100)
    h = (gravedad / 2) * t**2  # h = (1/2) * g * t^2
    plt.plot(t, h)
    plt.title('Simulación de Movimiento bajo Gravedad')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura (m)')
    plt.grid()
    plt.show()


def crear_mapa_calor(datos):
    sns.heatmap(datos, cmap='viridis')
    plt.title('Mapa de Calor')
    plt.show()
    
def Experimento():

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


#graficar sistema binario
def graficar_sistema_binario(duracion, intervalo):
    tiempo = np.arange(0, duracion, 0.1)  # Tiempo de 0 a 'duracion' con pasos de 0.1 segundos
    estado = []

    # Generar el estado del sistema binario
    for t in tiempo:
        if (t // (intervalo / 2)) % 2 == 0:
            estado.append(1)  # Estado encendido
        else:
            estado.append(0)  # Estado apagado

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, duracion)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('Comportamiento del Sistema Binario', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tiempo (s)', fontsize=12)
    ax.set_ylabel('Estado', fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Apagado', 'Encendido'])
    ax.grid(True)

    # Inicializar la línea que representará el estado
    line, = ax.plot([], [], lw=2, color='blue')

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de actualización para la animación
    def update(frame):
        x_data = tiempo[:frame]
        y_data = estado[:frame]
        line.set_data(x_data, y_data)
        return line,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(tiempo), init_func=init, blit=True, interval=100)

    plt.title('Comportamiento del Sistema Binario', fontsize=16, fontweight='bold')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.show()


#leyes de kepler
def animar_orbita(a, b, c, d):
    # Generar puntos para la elipse
    theta = np.linspace(0, 2 * np.pi, 100)
    x1 = a * np.cos(theta)  # Eje mayor
    y1 = b * np.sin(theta)  # Eje menor
    x2 = c * np.cos(theta)  # Eje mayor
    y2 = d * np.sin(theta)  # Eje menor

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='lightblue')
    ax.set_xlim(-max(a, c)-1, max(a, c)+1)
    ax.set_ylim(-max(b, d)-1, max(b, d)+1)
    ax.set_aspect('equal')
    ax.grid(color='white', linestyle='--', linewidth=0.5)  # Cuadrícula más sutil
    ax.set_title('Movimiento de Planetas en Órbita Elíptica', fontsize=16, fontweight='bold')
    ax.set_xlabel('Distancia (unidades astronómicas)', fontsize=12)
    ax.set_ylabel('Distancia (unidades astronómicas)', fontsize=12)

    # Añadir un fondo
    ax.set_facecolor('black')

    # Sol en el centro
    sun = plt.scatter(0, 0, color='gold', s=300, edgecolor='orange', label='Sol')  
    # Planeta 1
    planet1, = plt.plot([], [], 'o', color='blue', markersize=10, label='Planeta 1')  
    # Planeta 2
    planet2, = plt.plot([], [], 'o', color='red', markersize=10, label='Planeta 2')  

    # Función de inicialización
    def init():
        planet1.set_data([], [])
        planet2.set_data([], [])
        return planet1, planet2,

    # Función de actualización para la animación
    def update(frame):
        planet1.set_data(x1[frame], y1[frame])
        planet2.set_data(x2[frame], y2[frame])
        return planet1, planet2,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(x1), init_func=init, blit=True, interval=100)

    # Mostrar leyenda
    ax.legend(frameon=True, loc='upper right', fontsize=12, shadow=True)
    plt.show()

#graficar funciones trigonométricas
def graficar_funciones_trigonometricas(funcion, rango):
    x = np.linspace(rango[0], rango[1], 1000)  # Genera 1000 puntos en el rango especificado

    if funcion == 'seno':
        y = np.sin(x)
        plt.title('Gráfico de la función seno')
    elif funcion == 'coseno':
        y = np.cos(x)
        plt.title('Gráfico de la función coseno')
    elif funcion == 'tangente':
        y = np.tan(x)
        plt.title('Gráfico de la función tangente')
        plt.ylim(-10, 10)  # Limitar el rango de y para la tangente
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel(f'f(x) = {funcion}(x)')
        plt.grid()
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.show()
    else:
        hablar("Función no reconocida. Usa 'seno', 'coseno' o 'tangente'.")
        return



#movimientos de física
def simular_proyectil(velocidad, angulo, tiempo):
    g = 9.81  # Aceleración debido a la gravedad (m/s^2)

    # Convertir el ángulo a radianes
    angulo_rad = np.radians(angulo)

    # Calcular las componentes de la velocidad
    v_x = velocidad * np.cos(angulo_rad)
    v_y = velocidad * np.sin(angulo_rad)

    # Tiempo de vuelo
    t_vuelo = (2 * v_y) / g

    # Crear un array de tiempo
    t = np.linspace(0, min(t_vuelo, tiempo), num=100)

    # Ecuaciones de movimiento
    x = v_x * t
    y = (v_y * t) - (0.5 * g * t**2)

    # Crear la figura para la animación
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, max(x) + 1)
    ax.set_ylim(0, max(y) + 1)
    ax.set_title('Simulación del Lanzamiento del Proyectil')
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Altura (m)')
    ax.grid()

    # Inicializar la línea que representará el proyectil
    line, = ax.plot([], [], 'ro', markersize=10)  # Proyectil en rojo

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de actualización para la animación
    def update(frame):
        line.set_data(x[frame], y[frame])
        return line,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(x), init_func=init, blit=True, interval=100)

    plt.show()  # Mostrar la animación

    # Graficar la trayectoria final
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title('Trayectoria del Proyectil')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Altura (m)')
    plt.grid()
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.xlim(0, max(x) + 1)
    plt.ylim(0, max(y) + 1)
    plt.show()

def ejecutar_simulacion(velocidad, angulo, tiempo):
    try:
        velocidad = float(velocidad)
        angulo = float(angulo)
        tiempo = float(tiempo)

        simular_proyectil(velocidad, angulo, tiempo)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

def interfaz_usuario():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Simulación de Lanzamiento de Proyectil")

    # Crear etiquetas y entradas
    label_velocidad = tk.Label(ventana, text="Velocidad (m/s):")
    label_velocidad.pack()
    entry_velocidad = tk.Entry(ventana)
    entry_velocidad.pack()

    label_angulo = tk.Label(ventana, text="Ángulo (grados):")
    label_angulo.pack()
    entry_angulo = tk.Entry(ventana)
    entry_angulo.pack()

    label_tiempo = tk.Label(ventana, text="Tiempo de simulación (s):")
    label_tiempo.pack()
    entry_tiempo = tk.Entry(ventana)
    entry_tiempo.pack()

    # Botón para ejecutar la simulación
    boton_simular = tk.Button(ventana, text="Simular", command=lambda: ejecutar_simulacion(entry_velocidad.get(), entry_angulo.get(), entry_tiempo.get()))
    boton_simular.pack()

    # Iniciar la interfaz
    ventana.mainloop



def convertir_a_numero(texto):
    numeros = {
        'cero': 0,
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10
    }
    return numeros.get(texto, None)

#Convertir unidades
def convertir_unidad(valor, unidad_origen, unidad_destino):
    conversiones = {
        'metros a pies': valor * 3.28084,
        'pies a metros': valor / 3.28084,
        'kilómetros a millas': valor * 0.621371,
        'millas a kilómetros': valor / 0.621371,
        'grados Celsius a grados Fahrenheit': (valor * 9/5) + 32,
        'grados Fahrenheit a grados Celsius': (valor - 32) * 5/9,
    }
    
    clave = f"{unidad_origen} a {unidad_destino}"
    if clave in conversiones:
        return conversiones[clave]
    else:
        return None

def Creador():
    respuesta = ("Quién es mi creador?, pues, principalmente es Daniel. Pero sus amigos ayudaron con ideas para la creación del modelo a través de las funciones. ")
    hablar (respuesta)
    
def profe_jesus():
    respuesta_2 = ("¿qué?, ¿De quién hablas?, ¿Jesús garcia?, Ah, Okey, tu profesor de física, claro, cómo no acordarme de él. Señor, quiero decirle, que daniel está agradecido por dejarle participar en este pequeño evento, y quizás en un futuro no muy lejano pueda llegar a ser una buena Inteligencia artificial, solo que necesitaré bastante apoyo. Y no me pareció que haya pre informado a Daniel, oyó?. No mentira, es chiste jeje")
    hablar(respuesta_2)
def profe_jorge():
    respuesta_3 = ("Hola, como ya lo he dicho anteriormente, soy una inteligencia artificial diseñada para ayudar y asistir a los estudiantes en los ámbitos para los que he sido programada, tales como la física. Puedo ayudar en la búsqueda de conceptos, creacion de gráficas, y demás funciones interactivas. Así que, sin más qué decir, gracias")
    hablar(respuesta_3)




def despedirse():
    hablar(f"Hasta luego Señor, tenga un buen día, un gusto conocer a todas estas personas. Y ustedes muchachos cuídense.")

def escuchar_comando():

    with sr.Microphone() as source:
        print("Te escucho...")
        recognizer.adjust_for_ambient_noise(source,duration=1)


        try:

            audio = recognizer.listen(source,timeout=6,phrase_time_limit=5)
            
            texto = recognizer.recognize_google(audio,language='es')

            return texto.lower()
        


        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""



def hablar(texto):
    engine.say(texto)
    engine.runAndWait()
nombre_usuario = establecer_nombre_usuario()

if nombre_usuario:

    saludo = obtener_saludo()
    hora_actual = obtener_hora_actual()

    hablar(f"{saludo}, {nombre_usuario.capitalize()}!Son las {hora_actual}.¿En qué puedo servirte")
else:
    nombre_usuario = establecer_nombre_usuario()
    hablar(f"Mucho gusto cómo están Espectadores.{nombre_usuario.capitalize()}")





#GENERAR WEB
 # Configuración del puerto
    PORT = 8000
    server = None
    server_thread = None
def generar_web():
    import os
    import http.server
    import socketserver
    import threading
    from contextlib import suppress
    import customtkinter as ctk
    import webbrowser
    import atexit

    # Función para crear la página web
    def create_web_page(title, body_text, theme):
        folder_name = "Pagina Colmet"
        os.makedirs(folder_name, exist_ok=True)

        # Archivo HTML
        with open(os.path.join(folder_name, "index.html"), "w") as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <img src="data:image/jpeg;base64,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" alt="Colegio Metropolitano" width="400" height="400">
                <h1>{title}</h1>
                <p>{body_text}</p>
            </body>
            </html>
            """)

        # Archivo CSS
        with open(os.path.join(folder_name, "style.css"), "w") as f:
            if theme == "Claro":
                f.write("""
                body {
                    background-color: #fff;
                    color: #fff;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    color: #66d9ef;
                }

                p {
                    color: #ccc;
                }

                a {
                    color: #66d9ef;
                    text-decoration: none;
                }

                a:hover {
                    color: #fff;
                    text-decoration: underline;
                }

                button {
                    background-color: #444;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #555;
                }



                """)
            else:
                f.write("""
                body {
                    background-color: #333;
                    color: #333;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    color: #3498db;
                }

                p {
                    color: #666;
                }

                a {
                    color: #3498db;
                    text-decoration: none;
                }

                a:hover {
                    color: #2ecc71;
                    text-decoration: underline;
                }

                button {
                    background-color: #4CAF50;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #3e8e41;
                }
                """)

        # Iniciar servidor web
        start_web_server(folder_name)

    # Función para iniciar el servidor web
    def start_web_server(folder_name):
        global server, server_thread

        if server_thread and server_thread.is_alive():
            print("El servidor ya está corriendo.")
            return

        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=folder_name, **kwargs)

        server = socketserver.TCPServer(("localhost", PORT), CustomHandler)

        def run_server():
            with suppress(Exception):
                server.serve_forever()

        # Iniciar servidor en un hilo
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Registrar cierre del servidor al salir
        atexit.register(stop_web_server)

        # Abrir la página web automáticamente
        print(f"Servidor iniciado en http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")

    # Función para detener el servidor
    def stop_web_server():
        global server
        if server:
            server.shutdown()
            server.server_close()
            print("Servidor detenido.")

    # Interfaz gráfica con CustomTkinter
    def main():
        app = ctk.CTk()
        app.title("Generador de páginas web")
        app.geometry("1024x720")

        def generate_web_page():
            title = title_entry.get()
            body_text = body_entry.get("1.0", "end").strip()
            theme = theme_var.get()
            create_web_page(title, body_text, theme)

        # Widgets
        ctk.CTkLabel(app, text="Título de la página:").pack(pady=10)
        title_entry = ctk.CTkEntry(app)
        title_entry.pack()

        ctk.CTkLabel(app, text="Texto del cuerpo:").pack(pady=10)
        body_entry = ctk.CTkTextbox(app, height=50)
        body_entry.pack()

        theme_var = ctk.StringVar(value="Claro")
        ctk.CTkLabel(app, text="Tema:").pack(pady=10)
        ctk.CTkRadioButton(app, text="Claro", variable=theme_var, value="Claro").pack()
        ctk.CTkRadioButton(app, text="Oscuro", variable=theme_var, value="Oscuro").pack()

        generate_button = ctk.CTkButton(app, text="Generar Página Web", command=generate_web_page)
        generate_button.pack(pady=20)

        app.protocol("WM_DELETE_WINDOW", lambda: (stop_web_server(), app.destroy()))
        app.mainloop()

    if __name__ == "__main__":
        main()



while True:


    comando = escuchar_comando()


    if nombre_asistente.lower() in comando:

        hablar("¿En qué puedo ayudarte?")
    
    elif 'busca' in comando or 'buscar' in comando:
        busqueda = comando.replace('busca', '').replace('buscar', '').strip()
        hablar(f"Buscando {busqueda} en Google...")
        buscar_en_google(busqueda)


    elif 'quién es' in comando or 'quien es' in comando:
        person = comando.replace('quién es ', '').replace('quien es ', '')
        quien_es(person)
    elif 'qué es' in comando or 'que es' in comando:
        concepto = comando.replace('qué es ', '').replace('definir ', '').strip()
        definir_concepto(concepto)



    elif 'abre youtube' in comando or 'abrir youtube' in comando:
        abrir_youtube()
        hablar("abriendo youtube")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre facebook' in comando or 'abrir facebook' in comando:
        abrir_facebook()
        hablar("abriendo facebook")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre discord' in comando or 'abrir discord' in comando:
        abrir_discord()
        hablar("abriendo discord")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre whatsapp' in comando or 'abrir whatsapp' in comando:
        abrir_whatsapp()
        hablar("abriendo whastapp")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    
    elif 'abre instagram' in comando or 'abrir instagram' in comando:
        abrir_instagram()
        hablar("abriendo instagram")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")

    elif 'abre spotify' in comando or 'abrir spotify' in comando:
        abrir_spotify()
        hablar("abriendo spotify")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    elif 'abre tik tok' in comando or 'abrir tik tok' in comando:
        abrir_tiktok()
        hablar("abriendo tik tok")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    elif 'abre' in comando or 'abrir' in comando:
        aplicacion = comando.replace('abre', '').replace('abrir', '').strip()
        abrir_aplicacion(aplicacion)




#reproducir música
    elif 'reproduce' in comando:
        busqueda = comando.replace('reproduce', '')
        hablar("Reproduciendo en youtube "+busqueda)
        pywhatkit.playonyt(busqueda)
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")



#dar la hora
    elif'hora' in comando:
        hora_actual = obtener_hora_actual()
        hablar(f"la hora actual es{hora_actual}")
    


    elif 'sube el volumen' in comando or 'subir volumen' in comando:
        subir_volumen()


    elif 'baja el volumen' in comando or 'bajar volumen' in comando:
        bajar_volumen()

 

    #versículos y libros para la biblia    
    elif 'qué dice el versículo' in comando or 'que dice el versículo' in comando:
        libro, capitulo, versiculo, traduccion = comando.replace('qué dice el versículo', 'que dice el versículo' '').split()
        buscar_versiculo(libro, capitulo, versiculo, traduccion)

    elif 'busca libro' in comando:
        libro, traduccion = comando.replace('buscar libro', '').split()
        buscar_libro(libro, traduccion)






    #bromas
    elif 'cuéntame una broma' in comando or 'dime una broma' in comando:
        contar_broma()

 
 
    #gráficas, funciones, mapas de calor
    elif 'crea una función' in comando:
        hablar('graficando función')
        funcion = comando.replace('grafica una función', '').strip()
        rango = [-10, 10]  # Puedes ajustar el rango según sea necesario
        graficar_funcion(funcion, rango)
        hablar('en qué más le puedo ayudar')

    elif 'simula movimiento' in comando:
        hablar('Creando simulación')
        simular_movimiento()

    elif 'crea un mapa de calor' in comando:
        hablar('creando un mapa de calor')
        datos = np.random.rand(10, 10)  # Genera una matriz de 10x10 con datos aleatorios
        crear_mapa_calor(datos)
        hablar('en qué más puedo ayudar?')

    elif 'diseñar órbita' in comando:
        hablar("Diseñando órbita de los planetas")
        #Parámetros de la elipse
        a = 5 #semieje mayor del planeta 1
        b = 4 #semieje menor del planeta 1
        c = 3 #semieje mayor del planeta 2
        d = 2 #Semieje menor del planeta 2
        animar_orbita(a, b, c, d)


    elif 'simular lanzamiento de proyectil' in comando:
        hablar("Iniciando la interfaz de simulación de lanzamiento de proyectil.")
        interfaz_usuario()  # Llama a la interfaz de usuario
        hablar("He simulado el lanzamiento de un proyectil")


    # EXPERIMENTO FISICA
    elif 'iniciar experimento' in comando or 'simulación de parábola' in comando:
        hablar("Iniciando simulación de parábola en el aire")
        Experimento()
        hablar("""Simulación finalizada,
        esta simulacion, 
        desarrollada por Cervantes para contribuir en mis funcionalidades,
        representa el movimiento parablico, 
        una clase de fisica que, 
        en nuestro colegio fue dada por el profe Jesus Garcia.
        El movimiento parabólico es un tipo de movimiento que sigue una trayectoria en forma de parábola. 
        Ocurre cuando un objeto es lanzado hacia arriba y al frente, 
        bajo la influencia de la gravedad,
        y su desplazamiento se descompone en dos componentes
        ¿En qué más puedo ayudarte?""")

    #Deteccion facial
    elif 'detección de rostro' in comando or 'detección de cara' in comando:
        hablar("Iniciando la detección de rostro")
        from DeteccionFacial import detectar_puntos_rostro
        detectar_puntos_rostro()
        hablar("Detección de rostro finalizada")

    elif "crear historia" in comando:
        comando = escuchar_comando
        hablar("Déjame hacer volar la imaginación")
        print("creando historia")
        crear_historia()
        hablar("¿historia creada, quieres escucharla?")
        while True:
            try:
                if "escuchar historia" in comando():
                    hablar("La historia es la siguiente")
                    print("leyendo historia")
                    contar_historia()
                    break
            except:
                hablar("No entendí tu instruccion, prueba diciendo escuchar historia para escucharla, o hasta luego para terminar")

    elif "generar página web" in comando:
        hablar("Generando pagina web")
        generar_web()
        hablar("Pagina web generada")

    # OTROS
    elif 'hola' in comando or 'buenos dias' in comando or 'buenas tardes' in comando or 'buenas noches' in comando:
        hablar("Hola, ¿en qué puedo ayudarte")

    elif  'sistema binario' in comando or 'sistema binario' in comando:
        hablar("¿Cuál es la duración de la simulación en segundos? ")
        duracion_input = escuchar_comando()
        duracion = convertir_a_numero(duracion_input)
        if duracion is None:
            hablar("Lo siento, no entendí la duración. Por favor, usa números del cero al diez.")
            continue
        hablar("¿Cuál es el intervalo en segundo")
        intervalo_input = escuchar_comando()
        intervalo = convertir_a_numero(intervalo_input)
        if intervalo is None:
            hablar("Lo siento, no entendí el intervalo")
            continue
        graficar_sistema_binario(duracion, intervalo)
        hablar("He graficado el sistema binario. en qué más puedo ayudar?")



    elif 'función trigonométrica' in comando:
        hablar("¿Qué función trigonométrica deseas graficar? Puedes decir 'seno', 'coseno' o 'tangente'.")
        funcion_a_graficar = escuchar_comando()  # Escuchar la respuesta del usuario
        if 'seno' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función seno
            graficar_funciones_trigonometricas('seno', rango)
            hablar('graficando el seno')
        elif 'coseno' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función coseno
            graficar_funciones_trigonometricas('coseno', rango)
            hablar('graficando el coseno')
        elif 'tangente' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función tangente
            graficar_funciones_trigonometricas('tangente', rango)
            hablar('graficando la tangente')
        else:
            hablar("No entendí qué función deseas graficar.")



    # Aquí puedes definir cómo el usuario ingresará los datos para el mapa de calor
    # Por ejemplo, podrías pedirle que hable una matriz de datos o cargar un archivo
    # Para simplificar, aquí hay un ejemplo de datos aleatorios
    elif 'convierte' in comando:
        partes = comando.replace('convierte', '').strip().split(' a ')
        valor, unidad_origen = partes[0].strip().split()
        unidad_destino = partes[1].strip()
        valor = float(valor)
        resultado = convertir_unidad(valor, unidad_origen, unidad_destino)
        if resultado is not None:
            hablar(f"{valor} {unidad_origen} son {resultado} {unidad_destino}.")
        else:
            hablar("Lo siento, no puedo realizar esa conversión.")




    elif 'cuál es tu creador' in comando:
        Creador()

    elif 'dile algo' in comando:
        profe_jesus()

    elif 'saluda' in comando or 'saludar' in comando:
        profe_jorge()

    #despedidas
    elif 'gracias, adiós' in comando or 'hasta luego' in comando or 'chau' in comando:
        despedirse()
        break
    else:
        hablar("no entendí tu petición, ¿puedes repetir?, el margen de error que tengo es alto.")

