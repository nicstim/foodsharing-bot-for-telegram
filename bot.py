import telebot
from telebot import types
import requests
import sqlite3
import threading
import time
import bs4


# Функция парсера
def parser():
    pass


# Создание пользователя
def create_user(id,city):
    user = [id, city, "ALL"]
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user(user_id,city,push) VALUES(?,?,?)", user)
    con.commit()
    cur.close()
    con.close()



# Чтение информации о пользователе
def read_user(id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT push FROM user WHERE user_id = {id}")
    push, = cur.fetchone()
    cur.close()
    con.close()
    return push


# Обновление данных о пользователе
def update_user(id,push):
    pass



# user_id администратора бота.
admin_id = "270943665"

bot = telebot.TeleBot("1197512104:AAFbg4You7T1DHUOr3Ocklz4Z94qXtfHgoY")

print("bot start...")
# обработака /start
@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(True, False)
    menu.row("Профиль","Разместить объявление")
    bot.send_message(message.chat.id, f"""
Приветствую тебя,{message.from_user.first_name}.

Я фермер Mr. Foodsharing , добро пожаловать на мою ферму.
    """, reply_markup = menu)


# обработака /help
@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id,"""
Столкнулись с проблемой?
- Напишите в нашу службу поддержки: @lic_manager
    """)


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
