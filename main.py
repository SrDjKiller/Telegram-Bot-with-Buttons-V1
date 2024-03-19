import os
import time
import telebot
from telebot import types
import locale
from pytube import YouTube
import calendar
import com.get_events
import com.set_events
import com.random_events
import com.process_events
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

load_dotenv('env/.env')
TOKEN_BOT = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markupM = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Menu")
    markupM.add(item1)
    bot.reply_to(message, "Hola! Para ver los menu pulsa el boton que pone *Menu*" ".", reply_markup=markupM)

@bot.message_handler(func=lambda message: message.text == "Menu")
def show_commands(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Contar un chiste", callback_data='button1_pressed')
    markup.add(button1)
    button2 = types.InlineKeyboardButton("Ver todos los Eventos", callback_data='button2_pressed')
    markup.add(button2)
    button3 = types.InlineKeyboardButton("Ver eventos del Mes", callback_data='button3_pressed')
    markup.add(button3)
    button4 = types.InlineKeyboardButton("Ver eventos del Dia del Mes", callback_data='button4_pressed')
    markup.add(button4)
    button5 = types.InlineKeyboardButton("Enviar Foto", callback_data='button5_pressed')
    markup.add(button5)
    button6 = types.InlineKeyboardButton("YT", callback_data='button6_pressed')
    markup.add(button6)
    bot.send_message(message.chat.id, "¡Hola! En que te puedo ayudar!!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'button1_pressed':
        chat_id = call.message.chat.id
        chiste = com.random_events.contar_chiste(bot, chat_id)
        bot.send_message(chat_id, chiste)
    elif call.data == 'button2_pressed':
        chat_id = call.message.chat.id
        bot.reply_to(call.message, "Claro! Aquí tienes todos los eventos programados")        
        time.sleep(3)
        eventos = com.set_events.set_events(chat_id, bot)
        bot.send_message(chat_id, eventos)
    elif call.data == 'button3_pressed':
        chat_id = call.message.chat.id
        meses = [calendar.month_name[i] for i in range(1, 13)]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[str(i) for i in range(1, 13)])
        msg = bot.send_message(chat_id, "Por favor, selecciona el mes:", reply_markup=markup)
        bot.register_next_step_handler(msg, call_process_month)
    elif call.data == 'button4_pressed':
        chat_id = call.message.chat.id
        msg1 = bot.send_message(chat_id, "Por favor, escribe el DIA y el MES:")
        bot.register_next_step_handler(msg1, call_process_day) 
    elif call.data == 'button5_pressed':
        chat_id = call.message.chat.id
        photo_url = 'https://images.ecestaticos.com/GiZM0uLtgfwSCVN4cBP_LxR3T5Y=/0x0:2272x1278/1338x752/filters:fill(white):format(jpg)/f.elconfidencial.com%2Foriginal%2Fcd6%2F00f%2F373%2Fcd600f3737085d91d333ebb1dfcfcbb5.jpg'    
        bot.send_photo(chat_id, photo_url)
    elif call.data == 'button6_pressed':
        chat_id = call.message.chat.id
        video_url = "https://youtu.be/84WrDovUHtk?si=Q-rwTmLKaF8eTAch"
        bot.send_message(chat_id, f"Aquí tienes un video de YouTube: {video_url}")

def call_process_month(message):
    com.process_events.process_month(message, bot)

def call_process_day(message):
    com.process_events.process_day(message, bot)



bot.infinity_polling()
