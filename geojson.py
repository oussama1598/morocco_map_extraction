import requests
import json
import zipfile
import os

# mygeodata api keys
api_url = 'http://ogre.adc4gis.com/convertJson'

# regions data grabbed and transform from http://overpass-turbo.eu/s/RQz

regions = """Tanger-Tétouan-Al Hoceima ⵟⴰⵏⵊ-ⵟⵉⵜⴰⵡⵉⵏ-ⵍⵃⵓⵙⵉⵎⴰ طنجة-تطوان-الحسيمة
Oriental ⵜⴰⵏⴳⵎⵓⴹⵜ الشرقية
Drâa-Tafilalet ⴷⴰⵔⵄⴰ-ⵜⴰⴼⵉⵍⴰⵍⵜ درعة-تافيلالت
Souss-Massa ⵙⵓⵙⵙ-ⵎⴰⵙⵙⴰ سوس-ماسة
Guelmim-Oued Noun ⴳⵍⵎⵉⵎ-ⵡⴰⴷ ⵏⵓⵏ كلميم وادي نون
Casablanca-Settat ⵜⵉⴳⵎⵉ ⵜⵓⵎⵍⵉⵍⵜ-ⵙⵟⵟⴰⵜ الدار البيضاء-سطات
Marrakech-Safi ⵎⵕⵕⴰⴽⵛ-ⴰⵙⴼⵉ مراكش-أسفي
Laâyoune-Sakia El Hamra ⵍⵄⵢⵓⵏ-ⵙⴰⵇⵢⴰ ⵍⵃⴰⵎⵔⴰ العيون-الساقية الحمراء
Dakhla-Oued Ed-Dahab ⴷⴰⵅⵍⴰ-ⵡⴰⴷ ⴷⴰⵀⴰⴱ الداخلة-وادي الذهب
Rabat-Salé-Kénitra ⵔⴱⴰⵟ-ⵙⵍⴰ-ⵇⵏⵉⵟⵔⴰ الرباط-سلا-القنيطرة
Fès-Meknès ⴼⴰⵙ-ⵎⴽⵏⴰⵙ فاس-مكناس
Béni Mellal-Khénifra ⴰⵢⵜ ⵎⵍⵍⴰⵍ-ⵅⵏⵉⴼⵕⴰ بني ملال-خنيفرة""".split('\n')

for region in regions:
    # api for getting region boundaries
    api_url = f'https://nominatim.openstreetmap.org/search.php?q={region}&polygon_geojson=1&format=json'

    request = requests.get(api_url)

    data = json.loads(request.text)[0]
    region_name = data['display_name']
    geojson = data['geojson']

    print('Data retreived')

    with open(f'./geojson_data/{region}.json', 'w') as file:
        file.write(json.dumps(geojson))

for region in regions:
    print(f'Parsing {region}')

    geojson_data = open(f'./geojson_data/{region}.json', 'r').read()
    request = requests.post(
        api_url, data={'format': 'shp', 'json': geojson_data})

    print(f'Retreiving zip file for {region}')

    with open(f'./shp_data/{region}.zip', 'wb') as fd:
        for chunk in request.iter_content(1000):
            fd.write(chunk)

    print(f'Zip retrieved for {region}')

for region in regions:
    os.mkdir(f'./shp_files/{region}')

    with zipfile.ZipFile(f'./shp_data/{region}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'./shp_files/{region}')
