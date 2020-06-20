# -*- coding: utf-8 -*-
import requests
import time
import csv
import json

def take_1000_posts():
    token = '66efa73366efa73366efa733ea669d17a7666ef66efa73338034d48ba775c8f77625403'
    version = 5.92
    domain = 'foodsharing_spb'
    count = 2
    offset = 0
    all_posts = []

    while offset < 100:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                            )

        # data = response.json()
        # print(data)
        data = response.json()
        print(data)
        input()
        offset += 100
        all_posts.extend(data)
    return all_posts


def file_writer(data):
    with open('foodsharing_spb.csv', 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('body', 'url'))
        for post in data:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except:
                pass
            a_pen.writerow((post['text'], img_url))


all_posts = take_1000_posts()
file_writer(all_posts)
# print(all_posts)
