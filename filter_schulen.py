import json
import csv
from geopy.geocoders import Nominatim  # Neue Bibliothek importieren

schulen_liste = [
    "15 Schulen: Grundschulen",
    "16 Schulen: Mittelschulen",
    "17 Schulen: Realschulen",
    "18 Schulen: Gymnasien",
    "19 Schulen: Förderschulen",
    "21 Schulen: Weitere Schulen"
]
schulen_tuples = [(int(s.split()[0]), ' '.join(s.split()[2:])) for s in schulen_liste]
print(schulen_tuples)



schulen_dict = {int(s.split()[0]): ' '.join(s.split()[2:]) for s in schulen_liste}
print(schulen_dict)

import requests

url = "https://www.bildungsportal-a3.de/wp-admin/admin-ajax.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Accept": "*/*",
    "Content-Type": "multipart/form-data; boundary=---------------------------11876562914125794701181619007"
}

payload = (
    '-----------------------------11876562914125794701181619007\r\n'
    'Content-Disposition: form-data; name="action"\r\n\r\n'
    'mmp_map_markers\r\n'
    '-----------------------------11876562914125794701181619007\r\n'
    'Content-Disposition: form-data; name="type"\r\n\r\n'
    'map\r\n'
    '-----------------------------11876562914125794701181619007\r\n'
    'Content-Disposition: form-data; name="id"\r\n\r\n'
    '34,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,25,26,27,28,29,31,32\r\n'
    '-----------------------------11876562914125794701181619007\r\n'
    'Content-Disposition: form-data; name="custom"\r\n\r\n'
    'undefined\r\n'
    '-----------------------------11876562914125794701181619007\r\n'
    'Content-Disposition: form-data; name="lang"\r\n\r\n'
    '\r\n'
    '-----------------------------11876562914125794701181619007--\r\n'
)

response = requests.post(url, headers=headers, data=payload)
data = response.json()


# Datei einlesen
#with open('schulen-augsburg.json', 'r', encoding='utf-8') as file:
#    data = json.load(file)

# Nach maps Wert filtern 
filtered_features = [
    feature for feature in data['data']['features']
    if any(map_id in feature['properties']['maps'] for map_id in ['15', '16', '17', '18', '19', '21'])
]

geolocator = Nominatim(user_agent="schulen-augsburg")
# geolocator = Nominatim(user_agent="myapp")
        

# Ergebnisse ausgeben
for feature in filtered_features:
    props = feature['properties']
    location = geolocator.geocode(props['address'], addressdetails=True)
    print(location)
    if location and 'address' in location.raw:
        address = location.raw['address']
        name = address.get('house_number', '')
        strasse = address.get('road', '')
        plz = address.get('postcode', '')
        ort = address.get('city', address.get('town', address.get('village', '')))
    else:
        name = ''
        strasse = props['address']
        plz = ''
        ort = ''
    print(f"ID: {props['id']}")
    print(f"Name: {props['name']}")
    print(f"Maps: {props['maps']}")
    print(f"Adresse: {props['address']}")
    print(f"Name: {name}")
    print(f"Straße: {strasse}")
    print(f"PLZ: {plz}")
    print(f"Ort: {ort}")
    print(f"Erstellt am: {props['created_on_local_date']}")
    print("-" * 40)

# CSV-Datei speichern
with open('filtered_schulen.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID', 'Name', 'Maps', 'Adresse', 'Name', 'Straße', 'PLZ', 'Ort', 'Erstellt am']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for feature in filtered_features:
        props = feature['properties']
        location = geolocator.geocode(props['address'], addressdetails=True)
        if location:
            address = location.raw['address']
            name = address.get('house_number', '')
            strasse = address.get('road', '')
            plz = address.get('postcode', '')
            ort = address.get('city', address.get('town', address.get('village', '')))
        else:
            name = ''
            strasse = props['address']
            plz = ''
            ort = ''
        writer.writerow({
            'ID': schulen_dict.get(int(props['id']), props['id']),
            'Name': props['name'],
            'Maps': ', '.join([schulen_dict.get(int(map_id), map_id) for map_id in props['maps']]),
            'Adresse': props['address'],
            'Name': name,
            'Straße': strasse,
            'PLZ': plz,
            'Ort': ort,
            'Erstellt am': props['created_on_local_date']
        })