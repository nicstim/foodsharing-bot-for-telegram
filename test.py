# fruit = "яблоко"
#
# print(fruit[0:-2])
# from geopy.geocoders import Nominatim
# geolocator = Nominatim()
# location = geolocator.geocode("ulitsa Sedova, Saint Petersburg, Russia")
# # location = geolocator.geocode("Гущина 10 Псков")
# print(location.address)
# print((location.latitude, location.longitude))
import requests
import json

token = '66efa73366efa73366efa733ea669d17a7666ef66efa73338034d48ba775c8f77625403'
version = 5.92
domain = 'sharingfood'
count = 1
offset = 1
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
    print(response.json())
    data = response.json()['response']['items']

    offset += 10
    all_posts.extend(data)
for post in data:
    try:
        if post['attachments'][0]['type']:
            img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
        else:
            img_url = 'pass'
        print(post["user_id"])
    except:
        pass
