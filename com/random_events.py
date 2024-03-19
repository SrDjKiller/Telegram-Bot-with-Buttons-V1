import requests

def contar_chiste(bot, chat_id):
    try:
        response = requests.get('https://v2.jokeapi.dev/joke/Any?lang=es')
        data = response.json()
        if response.status_code == 200 and data['type'] == 'single':
            chiste = data['joke']
            return chiste
        elif response.status_code == 200 and data['type'] == 'twopart':
            setup = data['setup']
            delivery = data['delivery']
            chiste = chat_id, f"{setup}\n{delivery}"
            return chiste
        else:
            bot.send_message(chat_id, "¡Ups! No pude encontrar un chiste en este momento. Inténtalo de nuevo más tarde.")

    except Exception as e:
        bot.send_message(chat_id, "¡Ups! Ocurrió un error al obtener el chiste. Inténtalo de nuevo más tarde.")