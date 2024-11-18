import json
import csv

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


# Datei einlesen
with open('schulen-augsburg.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Nach maps Wert filtern 
filtered_features = [
    feature for feature in data['data']['features']
    if any(map_id in feature['properties']['maps'] for map_id in ['15', '16', '17', '18', '19', '21'])
]

# Ergebnisse ausgeben
for feature in filtered_features:
    props = feature['properties']
    print(f"ID: {props['id']}")
    print(f"Name: {props['name']}")
    print(f"Maps: {props['maps']}")
    print(f"Adresse: {props['address']}")
    print(f"Erstellt am: {props['created_on_local_date']}")
    print("-" * 40)
# CSV-Datei speichern
with open('filtered_schulen.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID', 'Name', 'Maps', 'Adresse', 'Erstellt am']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for feature in filtered_features:
        props = feature['properties']
        writer.writerow({
            'ID': schulen_dict.get(int(props['id']), props['id']),
            'Name': props['name'],
            'Maps': ', '.join([schulen_dict.get(int(map_id), map_id) for map_id in props['maps']]),
            'Adresse': props['address'],
            'Erstellt am': props['created_on_local_date']
        })