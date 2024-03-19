import calendar
import time
from telebot import types
import com.set_events

def process_month(message,bot):
    try:
        numero = int(message.text)
        partes = message.text.split()
        mes_numero = int(partes[-1])
        nombre_mes = calendar.month_name[mes_numero]
        nombre_mes = nombre_mes.capitalize()
        bot.reply_to(message, f"Claro! Aquí tienes todos los eventos programados para {nombre_mes}")
        time.sleep(3)
        eventos_mes = com.set_events.set_events_mes(message.chat.id, bot, message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Menu")
        markup.add(item1)
        bot.send_message(message.chat.id, "Te puedo ayudar en algo más?", reply_markup=markup)
        return eventos_mes
    except ValueError:
        bot.reply_to(message, "Por favor, ingresa un número válido.")

def process_day(message, bot):
    chat_id = message.chat.id
    numero = str(message.text)
    partes = message.text.split()
    dia_numero = int(partes[0])
    mes_numero = int(partes[-1])
    nombre_mes = calendar.month_name[mes_numero]
    nombre_mes = nombre_mes.capitalize()
    bot.reply_to(message, f"Claro! Aqui tienes todos los eventos programados para el dia {dia_numero} de {nombre_mes}")
    time.sleep(3)
    eventos_dia = com.set_events.set_events_dia(chat_id,bot,message)
    return eventos_dia




    # eventos_dia = com.set_events.set_events_dia(chat_id,bot,message)
    # return eventos_dia

