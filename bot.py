import telebot
from telebot import types
import requests
import sqlite3
import threading
import time


def take_posts():
    token = '66efa73366efa73366efa733ea669d17a7666ef66efa73338034d48ba775c8f77625403'
    version = 5.92
    domain = 'foodsharing_spb'
    count = 10
    offset = 0
    all_posts = []

    while offset < 10:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                            )

        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


fruits = ["яблоко", "бананы", "груша"]
vegetables = ["помидоры", "огурцы", "огурец"]

# Создание пользователя
def create_user(id,city):
    user = [id, city, "ALL", "None", "None", "None"]
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user(user_id,city,push,longitude,latitude,radius) VALUES(?,?,?,?,?,?)", user)
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


# Получение user_id всех пользователей
def read_all_user():
    pass


# Обновление данных о пользователе
def update_user(id,push):
    pass



# user_id администратора бота.
admin_id = "270943665"

bot = telebot.TeleBot("1197512104:AAFbg4You7T1DHUOr3Ocklz4Z94qXtfHgoY")

# Функция парсера
def parser():
    pass


print("bot start...")

# t_0 = threading.Thread(target = parser, name = "Парсер", args = (id,))

# обработака /start
@bot.message_handler(commands=['start'])
def start(message):
    global img_url
    menu = types.ReplyKeyboardMarkup(True, False)
    # menu.row("Профиль","Разместить объявление")
    set_city = types.InlineKeyboardMarkup(row_width = 2)
    spb = types.InlineKeyboardButton(text = "Санк-Петербург", callback_data = "spb")
    msk = types.InlineKeyboardButton(text = "Москва", callback_data = "msk")
    set_city.add(spb,msk)
    bot.send_message(message.chat.id, f"""
Приветствую тебя,{message.from_user.first_name}.

Меня зовут Mr. Foodsharing , добро пожаловать на мою ферму.
    """, reply_markup = set_city)

    # data = take_posts()
    # for post in data:
    #     try:
    #         if post['attachments'][0]['type']:
    #             img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
    #         else:
    #             img_url = 'pass'
    #     except:
    #         pass
    #     call_b = types.InlineKeyboardMarkup(row_width=1)
    #     btn1 = types.InlineKeyboardButton(text='Связаться', url = f"vk.com/id{post['signer_id']}" )
    #     call_b.add(btn1)
    #     try:
    #         bot.send_message(message.chat.id,f'{post["text"]}\n\n\n<a href="{img_url}">Фото</a>',parse_mode = "html" , reply_markup = call_b)
    #     except:
    #         bot.send_message(message.chat.id,f'{post["text"]}\n\n\n',parse_mode = "html" , reply_markup = call_b)


# обработака /help
@bot.message_handler(commands=['help'])
def start(message):
    id = str(message.from_user.id)
    bot.send_message(message.chat.id,"""
Столкнулись с проблемой?
- Напишите в нашу службу поддержки: @lic_manager
    """)


# Обработка текста
@bot.message_handler(content_types=['text'])
def body(message):
    if message.text == "Профиль":
        pass
    elif message.text == "Разместить объявление":
        pass


# Обработка локации
@bot.message_handler(content_types=['location'])
def location(local):
    if local:
        bot.send_message(local.from_user.id,local.location)



# обработка callback
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == "spb":
        city = "Санкт-Петербург"
        id = str(c.message.chat.id)
        create_user(id,city)
        bot.send_message(c.message.chat.id, c.message.chat.id)
    elif c.data == "msk":
        city = "Москва"
        id = str(c.message.chat.id)
        create_user(id,city)
        bot.send_message(c.message.chat.id, c.message.chat.id)


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
