"""
Módulo para manejar datos de Fórmula 1 usando la API Ergast.
"""
import requests

ERGAST_API_URL = "https://ergast.com/api/f1"

def obtener_calendario_f1():

    """Obtiene el calendario de carreras de la temporada actual."""
    try:
    
        url = f"{ERGAST_API_URL}/current.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        races = data['MRData']['RaceTable']['Races']
    
        calendario = [
            {
                'nombre': r['raceName'],
                'fecha': r['date'],
                'lugar': r['Circuit']['Location']['locality'] + ', ' + r['Circuit']['Location']['country']
            }
            for r in races
        ]
        return calendario
    
    except Exception as e:
        return f"Error al obtener el calendario de F1: {e}"

def obtener_clasificacion_pilotos():
    """Obtiene la tabla de puntos de pilotos de la temporada actual."""
    
    try:
    
        url = f"{ERGAST_API_URL}/current/driverStandings.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        tabla = [
            {
                'posicion': s['position'],
                'piloto': f"{s['Driver']['givenName']} {s['Driver']['familyName']}",
                'puntos': s['points'],
                'equipo': s['Constructors'][0]['name']
            }
            for s in standings
        ]
        return tabla
    
    except Exception as e:
        return f"Error al obtener la clasificación de pilotos: {e}"

def obtener_resultados_carrera(ano, ronda):
    """Obtiene los resultados de una carrera específica por año y ronda."""
    
    try:
    
        url = f"{ERGAST_API_URL}/{ano}/{ronda}/results.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data['MRData']['RaceTable']['Races'][0]['Results']
    
        resultados = [
            {
                'posicion': r['position'],
                'piloto': f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
                'equipo': r['Constructor']['name'],
                'tiempo': r.get('Time', {}).get('time', 'N/A')
            }
            for r in results
        ]
        return resultados
    
    except Exception as e:
        return f"Error al obtener resultados de la carrera: {e}"

def calcular_escenarios_campeonato(piloto):
    """Simula escenarios para que un piloto sea campeón (simplificado)."""
    
    try:
    
        tabla = obtener_clasificacion_pilotos()
    
        if isinstance(tabla, str):
    
            return tabla
    
        piloto_info = next((p for p in tabla if piloto.lower() in p['piloto'].lower()), None)
    
        if not piloto_info:
    
            return f"Piloto '{piloto}' no encontrado en la clasificación."
    
        puntos_actuales = float(piloto_info['puntos'])
        lider = tabla[0]
        puntos_lider = float(lider['puntos'])
        carreras_restantes = 22 - int(tabla[0]['posicion'])  # Suponiendo 22 carreras
        puntos_maximos = carreras_restantes * 25  # 25 puntos por victoria
    
        if puntos_actuales + puntos_maximos < puntos_lider:
            return f"{piloto_info['piloto']} ya no puede ser campeón matemáticamente."
    
        return f"{piloto_info['piloto']} necesita ganar {carreras_restantes} carreras y que {lider['piloto']} no sume más puntos para ser campeón."
    
    except Exception as e:
        return f"Error al calcular escenarios de campeonato: {e}"
