from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myapp")
location = geolocator.geocode("Grundschule Augsburg-Kriegshaber, Ulmer Straße 184A, 86156 Augsburg, Deutschland", addressdetails=True)
if location:
    parsed = location.raw['address']
    print(parsed)
else:
    print("Adresse nicht gefunden")