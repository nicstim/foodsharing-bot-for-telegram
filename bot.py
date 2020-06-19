import telebot
from telebot import types
import requests
import sqlite3
import smtplib
import threading

import parser

# user_id администратора бота.
admin_id = "270943665"

bot = telebot.TeleBot("1197512104:AAFbg4You7T1DHUOr3Ocklz4Z94qXtfHgoY")

print("bot start...")
# обработака /start
@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(True, False)
    menu.row("Профиль","Разместить объявление")
    bot.send_message(message.chat.id, "Привет!", reply_markup = menu)


# обработака /help
@bot.message_handler(commands=['help'])
def start(message):
    pass


# Обработка текста
@bot.message_handler(content_types=['text'])
def body(message):
    pass


# обработка callback
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    pass


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
