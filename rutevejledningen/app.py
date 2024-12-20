import folium
from folium import plugins
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Route til HTML-kortet
@app.route('/')
def map_view():
    return render_template('index.html')

@app.route('/map')
def int_map_view():
    return render_template('map_hospital_browser.html')

# Route til at servere GeoJSON
@app.route('/http://127.0.0.1:5000/')
def georesources(filename):
    return send_from_directory('/Rute_IoMT3/georesources', filename)

# GeoJSON-filer for bygning og sti
geo_resources = {
    'Hus65a': {
        'house': 'georesources/hus65a.geojson',
        'path': 'georesources/path_røntgen.geojson',
    },
    'Hus68': {
        'house': 'georesources/hus68.geojson',
        'path': 'georesources/path_kirurgi.geojson',
    },
}

# Kortets startkoordinater
hospital_coordinates = (54.778442742188595, 11.859601083623673)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_building = 'Hus68'  # Standardværdien
    if request.method == 'POST':
        selected_building = request.form['target']
    
    # Opret folium-kort
    map_hospital = folium.Map(location=hospital_coordinates, zoom_start=17, width="65%")
    
    # Hent geojson for den valgte bygning og sti
    house_file = geo_resources[selected_building]['house']
    path_file = geo_resources[selected_building]['path']
    
    # Tilføj bygning og sti til kortet
    with open(house_file, 'r') as f:
        house_data = json.load(f)
        folium.GeoJson(house_data).add_to(map_hospital)
    
    with open(path_file, 'r') as f:
        path_data = json.load(f)
        folium.plugins.AntPath(path_data['features'][0]['geometry']['coordinates']).add_to(map_hospital)

    # Gem kortet til en fil
    map_hospital.save("static/map_hospital.html")

    return render_template('index.html', selected_building=selected_building)


'''
def switchPosition(coordinate):
    """Skifter positionen fra [lng, lat] til [lat, lng]."""
    return [coordinate[1], coordinate[0]]
'''

@app.route('/update_map', methods=['POST'])
def update_map():
    selected_building = request.json['selected_building']

    # Hent geojson for den valgte bygning og sti
    house_file = geo_resources[selected_building]['house']
    path_file = geo_resources[selected_building]['path']

    # Læs GeoJSON-filerne
    with open(house_file, 'r') as f:
        house_data = json.load(f)
    
    with open(path_file, 'r') as f:
        path_data = json.load(f)

    '''
    # Konverter koordinater til [lat, lng]
    path_coordinates = [
]
        switchPosition(coord) for coord in path_data['features'][0]['geometry']['coordinates']
        
    ]
    '''
    # Byg GeoJSON til output
    return jsonify({
        'house_data': house_data,
        'path_data': path_data['features'][0]['geometry']['coordinates'],
    })

 
if __name__ == '__main__':
    app.run(debug=True)

