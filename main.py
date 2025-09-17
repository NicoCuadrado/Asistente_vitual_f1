"""
main.py - Punto de entrada del asistente virtual.
"""
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
from f1_handler import (

    obtener_calendario_f1,
    obtener_clasificacion_pilotos,
    obtener_resultados_carrera,
    calcular_escenarios_campeonato
)
from weather_handler import obtener_clima_por_ciudad
from calendar_handler import agendar_evento_google_calendar

# Inicialización de motor de voz
engine = pyttsx3.init()

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

def escuchar():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Escuchando...")
        audio = r.listen(source)
    
    try:
    
        texto = r.recognize_google(audio, language="es-ES")
        print(f"Usuario dijo: {texto}")
        return texto.lower()
    
    except Exception:
        hablar("No entendí, por favor repite.")
        return ""

def centro_pedido():

    hablar("¿En qué puedo ayudarte?")
    pedido = escuchar()

    if "cerrar" in pedido:

        hablar("Cerrando el asistente. ¡Hasta luego!")
        return False
    
    elif "calendario f1" in pedido:
    
        resultado = obtener_calendario_f1()
        hablar(str(resultado))
    
    elif "clasificación f1" in pedido:
    
        resultado = obtener_clasificacion_pilotos()
        hablar(str(resultado))
    
    elif "resultados f1" in pedido:
    
        hablar("¿De qué año?")
        ano = escuchar()
        hablar("¿De qué ronda?")
        ronda = escuchar()
        resultado = obtener_resultados_carrera(ano, ronda)
        hablar(str(resultado))
    
    elif "escenario campeonato" in pedido:
    
        hablar("¿Qué piloto?")
        piloto = escuchar()
        resultado = calcular_escenarios_campeonato(piloto)
        hablar(str(resultado))
    
    elif "clima" in pedido:
    
        hablar("¿De qué ciudad?")
        ciudad = escuchar()
        resultado = obtener_clima_por_ciudad(ciudad)
        hablar(str(resultado))
    
    elif "agendar evento" in pedido:
    
        hablar("Nombre del evento?")
        nombre = escuchar()
        hablar("Fecha y hora (YYYY-MM-DDTHH:MM:SS)?")
        fecha = escuchar()
        hablar("Lugar?")
        lugar = escuchar()
        resultado = agendar_evento_google_calendar(nombre, fecha, lugar)
        hablar(str(resultado))
    
    elif "abrir google" in pedido:
    
        webbrowser.open("https://www.google.com")
        hablar("Abriendo Google")
    
    else:
    
        hablar("No tengo esa funcionalidad aún.")
    
    return True

if __name__ == "__main__":
    # Ejemplo de interacción manual
    print("Ejemplo: obtener calendario F1")
    print(obtener_calendario_f1())
    print("Ejemplo: obtener clima de Buenos Aires")
    print(obtener_clima_por_ciudad("Buenos Aires"))
    print("Ejemplo: agendar evento en Google Calendar")
    # print(agendar_evento_google_calendar("Reunión", "2025-09-18T15:00:00", "Oficina"))
    # Para interacción por voz, descomentar:
    ejecutando = True
    while ejecutando:
        ejecutando = centro_pedido()
