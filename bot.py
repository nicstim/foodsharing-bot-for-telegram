import telebot
from telebot import types
import requests
import sqlite3
import threading
import time
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import re
def get_subway():
    subway = []
    con = sqlite3.connect("spb.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM subway ORDER BY name")
    sub = cur.fetchall()
    for i in range(0,len(sub),1):
        s = str(sub[i])
        for char in s:
            if char == ',' or char == '(' or char == ')' or char == "'":
                s = s.replace(char,'')
            else:
                pass
        subway.append(s)
    cur.close()
    con.close()
    return subway

print(len(get_subway()))
def get_street():
    street = []
    con = sqlite3.connect("spb.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM street ORDER BY name")
    sub = cur.fetchall()
    for i in range(0,len(sub),1):
        s = str(sub[i])
        for char in s:
            if char == ',' or char == '(' or char == ')' or char == "'":
                s = s.replace(char,'')
            else:
                pass
        street.append(s)
    cur.close()
    con.close()
    return street

print(len(get_street()))
# Разбиение на слова
def get_word(string):
    return re.split('\W+', string)


def getdist(s1, s2):
    d, len_s1, len_s2 = {}, len(s1), len(s2)
    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1
    for i in range(len_s1):
        for j in range(len_s2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,
                d[(i, j - 1)] + 1,
                d[(i - 1, j - 1)] + cost)
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
    return(d[len_s1 - 1, len_s2 - 1])


def check_sub(search_request, original_text, max_distance):
    substring_list_1 = get_word(search_request)
    substring_list_2 = get_word(original_text)

    not_found_count = len(substring_list_1)

    for substring_1 in substring_list_1:
        for substring_2 in substring_list_2:
            if getdist(substring_1, substring_2) <= max_distance:
                not_found_count -= 1

    if not not_found_count:
        return True


def take_posts_spb():
    global subway_result
    global street_result
    global img_url
    global last_text
    global old_last_text
    global post_lat
    global post_long
    subways = get_subway()
    streets = get_street()
    token = '7a7053df7a7053df7a7053dfd97a02e6c777a707a7053df249efa94a70db50ab3b1c74c'
    version = 5.92
    domain = 'foodsharing_spb'
    count = 5
    offset = 1
    last_text = ""
    old_last_text = ""
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


            if last_text == str(post["text"]) or old_last_text == str(post["text"]):
                break
            else:



                for i in range(0,len(users_id),1):
                    id = str(users_id[i])
                    for char in id:
                        if char == ',' or char == '(' or char == ')' or char == "'":
                            id = id.replace(char,'')
                        else:
                            pass
                    read_user(id)
                    try:
                        post_lat = post['attachments'][0]['photo']['lat']
                        post_long = post['attachments'][0]['photo']['long']
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
                                        # post_lat = post['attachments'][0]['photo']['lat']
                                        # post_long = post['attachments'][0]['photo']['long']
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
                    except:
                        street_result = False
                        subway_result = False
                        original = str(post["text"])
                        for subway in subways:
                            # print(subway)
                            subway_result = check_sub(subway, original, max_distance=2)
                            if subway_result == True:
                                original = "text"
                                if push == "LOCAL":
                                    geolocator = Nominatim()
                                    location = geolocator.geocode(f"{subway} Питер")
                                    post_lat = float(location.latitude)
                                    post_long= float(location.longitude)
                                    post_local = (post_lat, post_long)
                                    user_local = (latitude,longitude)
                                    distance = float(great_circle(post_local, user_local).miles)
                                    if float(radius) >= distance:
                                        try:
                                            print(f"subway True {subway}")
                                            call_b = types.InlineKeyboardMarkup(row_width=1)
                                            btn1 = types.InlineKeyboardButton(text='Связаться', url = f"vk.com/id{post['signer_id']}" )
                                            call_b.add(btn1)
                                            try:
                                                bot.send_message(id,f'Рядом с вами!\n\n{post["text"]}\n\n\n<a href="{img_url}">Фото</a>',parse_mode = "html" , reply_markup = call_b)
                                                # bot.send_location(id,post_lat,post_long)
                                            except:
                                                bot.send_message(id,f'Рядом с вами!\n\n{post["text"]}', reply_markup = call_b)
                                            try:
                                                bot.send_location(id,post_lat,post_long)
                                            except:
                                                pass
                                        except Exception as e:
                                            print(e)
                        if subway_result == False:
                            original = str(post["text"])
                            for street in streets:
                                street_result = check_sub(street, original, max_distance=2)
                                if street_result == True:
                                    original = "text"
                                    if push == "LOCAL":
                                        geolocator = Nominatim()
                                        location = geolocator.geocode(f"{street} Питер")
                                        post_lat = float(location.latitude)
                                        post_long= float(location.longitude)
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
                        else:
                            pass

                    if iter == 0:
                        last_text = str(post["text"] )
                        print('last text save')
                        iter +=1

                    if z == 0 and last_text != str(post["text"]) :
                        old_last_text = last_text
                        last_text = str(post["text"]  )
                        print('last text update')
                    z +=1

        continue
        time.sleep(600) # 10 минут
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


# Обновление данных о пользователе
def update_user(id,push):
    pass



# user_id администратора бота.
admin_id = "270943665"

bot = telebot.TeleBot("1197512104:AAFbg4You7T1DHUOr3Ocklz4Z94qXtfHgoY")



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
