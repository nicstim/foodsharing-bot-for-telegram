import telebot
from telebot import types
import requests
import sqlite3
import threading
import time
from geopy.distance import great_circle


def take_posts_spb():
    global img_url
    global last_text
    token = 'd7c00a0bd7c00a0bd7c00a0b52d7b2bea4dd7c0d7c00a0b892e788753a751b66f4ec2e2'
    version = 5.92
    domain = 'foodsharing_spb'
    count = 5
    offset = 1
    last_text = ""
    all_posts = []

    iter = 0
    while True:

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
        all_posts.extend(data)
        z = 0
        for post in data:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except:
                img_url = 'pass'
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT user_id FROM user WHERE city = 'Санкт-Петербург'")
            users_id = cur.fetchall()
            cur.close()
            con.close()
            if last_text == str(post["text"]):
                break
            else:

                for i in range(0,len(users_id),1):
                    id = str(users_id[i])
                    for char in id:
                        if char == ',' or char == '(' or char == ')' or char == "'":
                            id = id.replace(char,'')
                        else:
                            pass


                    if iter == 0:
                        last_text = str(post["text"] )
                        print('last text save')
                        iter +=1

                    read_user(id)
                    if push == "ALL":
                        print("all")
                        try:
                            try:
                                call_b = types.InlineKeyboardMarkup(row_width=1)
                                btn1 = types.InlineKeyboardButton(text='Связаться', url = f"vk.com/id{post['signer_id']}" )
                                call_b.add(btn1)
                                try:
                                    bot.send_message(id,f'{post["text"]}\n\n\n<a href="{img_url}">Фото</a>',parse_mode = "html" , reply_markup = call_b)
                                except:
                                    bot.send_message(id,f'{post["text"]}', reply_markup = call_b)
                                try:
                                    post_lat = post['attachments'][0]['photo']['lat']
                                    post_long = post['attachments'][0]['photo']['long']
                                    bot.send_location(id,post_lat,post_long)
                                except:
                                    pass
                            except Exception as e:
                                print(e)

                        except:
                            pass

                    elif push == "LOCAL":
                        print("local")
                        try:
                            post_lat = post['attachments'][0]['photo']['lat']
                            post_long = post['attachments'][0]['photo']['long']
                            post_local = (post_lat, post_long)
                            user_local = (latitude,longitude)
                            distance = float(great_circle(post_local, user_local).miles)
                            if float(radius) >= distance:
                                try:
                                    call_b = types.InlineKeyboardMarkup(row_width=1)
                                    btn1 = types.InlineKeyboardButton(text='Связаться', url = f"vk.com/id{post['signer_id']}" )
                                    call_b.add(btn1)
                                    try:
                                        bot.send_message(id,f'Рядом с вами!\n\n{post["text"]}\n\n\n<a href="{img_url}">Фото</a>',parse_mode = "html" , reply_markup = call_b)
                                        bot.send_location(id,post_lat,post_long)
                                    except:
                                        bot.send_message(id,f'Рядом с вами!\n\n{post["text"]}', reply_markup = call_b)
                                        bot.send_location(id,post_lat,post_long)
                                except Exception as e:
                                    print(e)

                        except:
                            pass

                    else:
                        pass
                    if z == 0 and last_text != str(post["text"]) :
                        last_text = str(post["text"]  )
                        print('last text update')
                    z +=1

        continue
        time.sleep(210) # 3.5 минуты
    print("end")


def update_local(id, latitude,longitude):
    con = sqlite3.connect("databas.db")
    cur = con.cursor()
    cur.execute(f"UPDATE user SET latitude ={latitude} WHERE user_id ={id}")
    cur.execute(f"UPDATE user SET longitude ={longitude} WHERE user_id ={id}")
    cur.close()
    con.close()


def update_radius(id,r):
    con = sqlite3.connect("databas.db")
    cur = con.cursor()
    cur.execute(f"UPDATE user SET radius ={r} WHERE user_id ={id}")
    cur.close()
    con.close()

fruits = ["яблоко", "бананы", "груша"]
vegetables = ["помидоры", "огурцы", "огурец"]

# Создание пользователя
def create_user(id):
    user = [id, "Санкт-Петербург", "ALL", "None", "None", "5"]
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user(user_id,city,push,longitude,latitude,radius) VALUES(?,?,?,?,?,?)", user)
    con.commit()
    cur.close()
    con.close()



# Чтение информации о пользователе
def read_user(id):
    global push
    global radius
    global city
    global longitude
    global latitude
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # push
    cur.execute(f"SELECT push FROM user WHERE user_id = {id}")
    push, = cur.fetchone()
    # radius
    cur.execute(f"SELECT radius FROM user WHERE user_id = {id}")
    radius, = cur.fetchone()
    # city
    cur.execute(f"SELECT city FROM user WHERE user_id = {id}")
    city, = cur.fetchone()
    # longitude
    cur.execute(f"SELECT longitude FROM user WHERE user_id = {id}")
    longitude, = cur.fetchone()
    # latitude
    cur.execute(f"SELECT latitude FROM user WHERE user_id = {id}")
    latitude, = cur.fetchone()

    cur.close()
    con.close()


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

t_0 = threading.Thread(target = take_posts_spb, name = "Парсер", args = ())
t_0.start()

# обработака /start
@bot.message_handler(commands=['start'])
def start(message):
    id = str(message.from_user.id)
    try:
        read_user(id)
        print(city)
    except:
        create_user(id)

    # menu = types.ReplyKeyboardMarkup(True, False)
    # # menu.row("Профиль","Разместить объявление")
    bot.send_message(message.chat.id, f"""
Приветствую тебя,{message.from_user.first_name}.

Меня зовут Mr. Foodsharing , добро пожаловать на мою ферму.
    """)


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
        menu = types.ReplyKeyboardMarkup(True, False)
        menu.row("Профиль","Разместить объявление")
        long = local.location.longitude
        lat = local.location.latitude
        bot.send_message(local.from_user.id,f"Ваше местоположение определенно.\n Широта: {lat} Долгота: {long}",reply_markup = menu)



# обработка callback
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    pass

bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
