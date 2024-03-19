import com.get_events

def set_events(chat_id,bot):
    events = com.get_events.get_calendar_events()
    for event in events:
        formatted_start_time_str = event[0]
        event_summary = event[1]
        bot.send_message(chat_id, f"************************************\nFecha: {formatted_start_time_str}\nEvento: {event_summary}\n************************************")
    if not events:
        bot.send_message(chat_id, "No hay eventos.")

def set_events_mes(chat_id,bot,message):
    month = int(message.text.split()[0])
    events = com.get_events.get_events_for_month(month)
    try:
        if month < 1 or month > 12:
            raise ValueError("El mes debe estar entre 1 y 12")
        if events:
            for event in events:
                formatted_start_time_str = event[0]
                event_summary = event[1]
                bot.send_message(chat_id, f"************************************\nFecha: {formatted_start_time_str}\nEvento: {event_summary}\n************************************")
        else:
            bot.send_message(chat_id, "No hay eventos para ese mes.")
    except (IndexError, ValueError):
        bot.send_message(chat_id, "Por favor, utiliza el formato /eventosmes donde el mes es un número entre 1 y 12.")

def set_events_dia(chat_id,bot,message):
    try:
        # Dividir el mensaje en partes separadas por espacios
        day, month = message.text.split()
        day = int(day)
        month = int(month)

        # Verificar si el día y el mes están dentro de los rangos válidos
        if day < 1 or day > 31:
            raise ValueError("El día debe estar entre 1 y 31")
        if month < 1 or month > 12:
            raise ValueError("El mes debe estar entre 1 y 12")

        # Obtener los eventos para el día y el mes especificados
        events = com.get_events.get_events_for_day(day, month)

        if events:
            for event in events:
                formatted_start_time_str = event[0]
                event_summary = event[1]
                bot.send_message(chat_id, f"************************************\nFecha: {formatted_start_time_str}\nEvento: {event_summary}\n************************************")
        else:
            bot.send_message(chat_id, "No hay eventos para ese día.")
    except (IndexError, ValueError):
        bot.send_message(chat_id, "Por favor, utiliza el formato /eventosdia <día> <mes> donde el día entre 1 y 31 y el mes es un número entre 1 y 12.")