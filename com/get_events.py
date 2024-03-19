import datetime, re
import googleapiclient.discovery
import google.auth
 
# Preparation for Google API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = 'CALENDAR IDA'
gapi_creds = google.auth.load_credentials_from_file('config/credenciales.json', SCOPES)[0]
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
fecha_actual = datetime.datetime.now()
año_actual = fecha_actual.year

def get_calendar_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    formatted_events = []
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date', 'Fecha no especificada'))
        formatted_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        formatted_start_time_str = formatted_start_time.strftime('%d/%m/%Y')
        event_summary = event.get('summary', 'Evento sin título')
        formatted_events.append((formatted_start_time_str, event_summary))
    return formatted_events

def get_events_for_month(month):
    try:
        start_date = datetime.date(año_actual, month, 1)
        if month == 12:
            end_date = datetime.date(año_actual, 12, 31)
        else:
            end_date = datetime.date(año_actual, month + 1, 1) - datetime.timedelta(days=1)
        start_time = start_date.isoformat() + 'T00:00:00Z'
        end_time = end_date.isoformat() + 'T23:59:59Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        formatted_events = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date', 'Fecha no especificada'))
            formatted_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            formatted_start_time_str = formatted_start_time.strftime('%d/%m/%Y')
            
            event_summary = event.get('summary', 'Evento sin título')
            formatted_events.append((formatted_start_time_str, event_summary))
        return formatted_events

    except Exception as e:
        return f"Error al obtener eventos del mes: {e}"

def get_events_for_day(month, day):
    try:
        fecha = datetime.date(año_actual, day, month)
        start_time = fecha.isoformat() + 'T00:00:00Z'
        end_time = fecha.isoformat() + 'T23:59:59Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        formatted_events = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date', 'Fecha no especificada'))
            formatted_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            formatted_start_time_str = formatted_start_time.strftime('%d/%m/%Y')
            event_summary = event.get('summary', 'Evento sin título')
            formatted_events.append((formatted_start_time_str, event_summary))
        return formatted_events

    except Exception as e:
        return f"Error al obtener eventos del día: {e}"
    