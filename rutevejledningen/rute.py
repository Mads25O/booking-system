import folium 
from folium import plugins
import pandas as pd

import ipywidgets
import os
import json


#opret map

hospital_coordinates = (54.778442742188595, 11.859601083623673)

map_hospital = folium.Map(location=hospital_coordinates, width="65%", zoom_start=17)

#indsæt geojson data om house outline
houseOutline = r'/georesources/hus68.geojson'
(folium.GeoJson(houseOutline, name="hus68").add_to(map_hospital))


#indsæt geojson data om antpath
path_geojson = r'/georesources/path_kirurgi.geojson'

def switchPosition(coordinate):
  temp = coordinate[0]
  coordinate[0] = coordinate[1]
  coordinate[1] = temp
  return coordinate

with open(path_geojson) as f:
  way = json.load(f)

for feature in way['features']:
    path = feature['geometry']['coordinates']
final_path = list(map(switchPosition,path))
final_path
     
path = r'/georesources/path_kirurgi.geojson'
folium.plugins.AntPath(
    [
    [54.77883321572841, 11.859981479044592],
    [54.77867923314005, 11.85987800960902],
    [54.778671929031134, 11.85968266406664],
    [54.77863560665898, 11.859519887053722],
    [54.77854975883673, 11.859191162353909],
    [54.77848889521417, 11.858958988485995],
    [54.77830293034427, 11.858676148356778]
]
).add_to(map_hospital)

map_hospital.save("map_hospital.html")


# GeoJSON-filer for bygning og sti
# geo_resources = {
#     'Hus65a': {
#         'house':'C:/Users/amali/OneDrive - Københavns Erhvervsakademi/Skrivebord/Rute_IoMT3/georesources/hus65a.geojson',
#         'path': 'C:/Users/amali/OneDrive - Københavns Erhvervsakademi/Skrivebord/Rute_IoMT3/georesources/path_røntgen.geojson',
#     },
#     'Hus68': {
#         'house': 'C:/Users/amali/OneDrive - Københavns Erhvervsakademi/Skrivebord/Rute_IoMT3/georesources/hus68.geojson',
#         'path': 'C:/Users/amali/OneDrive - Københavns Erhvervsakademi/Skrivebord/Rute_IoMT3/georesources/path_kirurgi.geojson',
#     },
# }

# # Funktion til at opdatere kortet
# def update_map(selected_building):
# # Ryd kortet
#     map_hospital = folium.Map(location=hospital_coordinates, width="65%", zoom_start=17)

#     # Hent den valgte bygning og sti
#     house_file = geo_resources[selected_building]['house']
#     path_file = geo_resources[selected_building]['path']

# # Tilføj hus og sti til kortet
#     with open(house_file, 'r') as f:
#         house_data = json.load(f)
#         folium.GeoJson(house_data, name=selected_building).add_to(map_hospital)
    
#     with open(path_file, 'r') as f:
#         path_data = json.load(f)
#         path_coordinates = path_data['features'][0]['geometry']['coordinates']

#     return map_hospital


# Dynamisk dropdown-menu med JavaScript
# dropdown_html = """
# <div style="position: fixed; 
#             top: 10px; left: 10px; width: 200px; z-index: 9999; 
#             background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;">
#   <label for="start">Startpunkt:</label><br>
#   <select id="start" onchange="updateRoute()">
#     <option value="w" selected>Indgang</option>
#   </select><br><br>
  
#   <label for="target">Målpunkt:</label><br>
#   <select id="target" onchange="updateRoute()">
#     <option value="Hus1">Hus1</option>
#     <option value="Hus15">Hus15</option>
#     <option value="Hus15a">Hus15a</option>
#     <option value="Hus15b">Hus15b</option>
#     <option value="Hus62b">Hus62b</option>
#     <option value="Hus64">Hus64</option>
#     <option value="Hus65a">Hus65a</option>
#     <option value="Hus66">Hus66</option>
#     <option value="Hus68" selected>Hus68</option>
#   </select>
# </div>

# <script>
#   // JavaScript funktion til at opdatere ruten
#   function updateRoute() {
#     const start = document.getElementById("start").value;
#     const target = document.getElementById("target").value;
#     alert("Rute opdateret fra: " + start + " til: " + target);
#     // TODO: Tilføj logik til at opdatere kortets stier
#   }
# </script>
# """

# # # Tilføj dropdown til kortet som et HTML-element
# # folium.Marker(
# #     location=hospital_coordinates,
# #     icon=folium.DivIcon(html=dropdown_html)
# # ).add_to(map_hospital)

# # # Funktion til at opdatere kortet baseret på valgte bygning
# # def update_map(selected_building):
# #     # Ryd kortet
# #     map_hospital = folium.Map(location=hospital_coordinates, width="65%", zoom_start=17)

# # # Hent den valgte bygning og sti
# #     house_file = geo_resources[selected_building]['house']
# #     path_file = geo_resources[selected_building]['path']

# #     # Tilføj hus og sti til kortet
# #     with open(house_file, 'r') as f:
# #         house_data = json.load(f)
# #         folium.GeoJson(house_data, name=selected_building).add_to(map_hospital)

# #     with open(path_file, 'r') as f:
# #         path_data = json.load(f)
# #         folium.plugins.AntPath(path_data['features'][0]['geometry']['coordinates']).add_to(map_hospital)

# #     return map_hospital

# map_hospital.save("map_hospital.html")

# #Interaktivitet
# '''
# select_widget=ipywidgets.Select(
#     options=['Option A', 'Option B'],
#     value='Option A',
#     description='Select',
#     disabled=False)

# def selectOption(opt):
#     if opt == 'Option A':
#         print('A')
#     if opt == 'Option B':
#         print('B')
# ipywidgets.interact(selectOption, opt=select_widget)

# #byg navigatoren

# class navigator:
#     def __init__(self):
#         self.geo_resources = {}
#         self.hospital_location =(54.778442742188595, 11.859601083623673)
#         self.position = 'w'
#         self.destination = 'Hus 68'

#         for root, dirs, files in os.walk('C:/Users/amali/OneDrive - Københavns Erhvervsakademi/Skrivebord/Rute_IoMT3/georesources'):  
#             for file in files:
#                 self.geo_resources[file.split('.')[0]] = root+'/'+file

#     def changeDestination(self,newDestination):
#         self.destination = newDestination
#         self.redrawMap()

#     def changeStartPoint(self, newStartPoint):
        
#         #self.position = newStartPoint #does not work yet
#         print(f'Selected Start: {newStartPoint}; Selected Target: {self.destination}')
#         #self.redrawMap()
        
#     def drawPathWay(self, hospital_map):
      
#         def switchPosition(coordinate):
#             temp = coordinate[0]
#             coordinate[0] = coordinate[1]
#             coordinate[1] = temp
#             return coordinate

#         searchString = self.position + self.destination.split('Hus')[1]
#         with open(self.geo_resources[searchString]) as f:
#            testWay = json.load(f)

#         for feature in way['features']:
#             path = feature['geometry']['coordinates']

#             final_path = list(map(switchPosition,path))
#             folium.plugins.AntPath(final_path).add_to(hospital_map)

#     def drawBuilding(self,hospital_map):
#       houseOutline = self.geo_resources[self.destination]
#       folium.GeoJson(houseOutline, name="geojson").add_to(hospital_map)

#     def redrawMap(self):
#         #print(f'position {self.position}, destination {self.destination}')
#         hospital_map = folium.Map(location = self.hospital_location, width = "75%", zoom_start = 17)
#         self.drawPathWay(hospital_map)
#         self.drawBuilding(hospital_map)


# my_navigator = navigator()

# def display_way(where_to):
#      my_navigator.changeDestination(where_to)

# def change_position(where_from):
#     my_navigator.change_start_point(where_from)

# # Destination Selector
# select_house_widget=ipywidgets.Select(
    
# options=['Hus1',
#     'Hus15',
#     'Hus15a',
#     'Hus15b',
#     'Hus62b',
#     'Hus64',
#     'Hus65a',
#     'Hus66',
#     'Hus68'],
#     value='Hus1',
#     description='Target',
#     disabled=False)

# # widget function
# def select_house(way):
#     if way == 'Hus15' :
#         display_way('Hus15' ) 
#     if way == 'Hus15a':
#         display_way('Hus15a')
#     if way == 'Hus15b':
#         display_way('Hus15b')
#     if way == 'Hus62b':
#         display_way('Hus62b')
#     if way == 'Hus64':
#         display_way('Hus64')
#     if way == 'Hus65a':
#         display_way('Hus65a')
#     if way == 'Hus66':
#         display_way('Hus66')
#     if way == 'Hus68':
#         display_way('Hus68')

# # Position Selector
# select_position_widget=ipywidgets.Select(
#     options=['Indlæggelse', 'Indgang vest', 'Indgang øst', 'Indgang til køretøjer'],
#     value='Indgang vest',
#     description='Start',
#     disabled=False)

# def select_position(position):
#     if position == 'Indlæggelse':
#         change_position('a')
#     if position == 'Indgang vest':
#         change_position('w')
#     if position == 'Indgang øst':
#         change_position('o')
#     if position == 'Indgang til køretøjer':
#         change_position('f')

# #Initialization   
# ipywidgets.interact(select_position, position=select_position_widget)
# ipywidgets.interact(select_house, way=select_house_widget)
# '''


