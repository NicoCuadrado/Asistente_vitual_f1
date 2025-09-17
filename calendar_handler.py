"""
Módulo para agendar eventos en Google Calendar usando google-api-python-client y OAuth2.
"""
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def agendar_evento_google_calendar(nombre_evento, fecha, lugar):

    """Crea un evento en Google Calendar."""
    creds = None

    if os.path.exists('token.pickle'):

        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        
        if creds and creds.expired and creds.refresh_token:
        
            creds.refresh(Request())
        
        else:
        
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    try:
    
        service = build('calendar', 'v3', credentials=creds)
        evento = {
            'summary': nombre_evento,
            'location': lugar,
            'start': {
                'dateTime': fecha,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': fecha,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
        }
    
        evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
        return f"Evento creado: {evento_creado.get('htmlLink')}"
    
    except Exception as e:
        return f"Error al agendar evento: {e}"
