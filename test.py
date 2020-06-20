# fruit = "яблоко"
#
# print(fruit[0:-2])
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("ulitsa Sedova, Saint Petersburg, Russia")
# location = geolocator.geocode("Гущина 10 Псков")
print(location.address)
print((location.latitude, location.longitude))
