"""
Módulo para obtener el clima usando la API de OpenWeatherMap.
"""
import requests

OPENWEATHER_API_KEY = "fb3f9b705b95cbfcd3e28988beda9dfa"  #API Key
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def obtener_clima_por_ciudad(ciudad):
    """Obtiene el pronóstico del clima para una ciudad."""
    try:

        params = {
            'q': ciudad,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        clima = {
            'ciudad': data['name'],
            'pais': data['sys']['country'],
            'temperatura': data['main']['temp'],
            'descripcion': data['weather'][0]['description'],
            'humedad': data['main']['humidity'],
            'viento': data['wind']['speed']
        }
        
        return clima
    
    except Exception as e:
        return f"Error al obtener el clima: {e}"
