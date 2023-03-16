import os
import json
import requests
import folium
from geopy import distance
from flask import Flask


def coffee_map():
    with open('index.html') as file:
        return file.read()


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()[
        'response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_coffe_dist(rezult_coffee_list):
    return rezult_coffee_list['distance']


def rezult_coffe_list(coordinates_user):
    rezult_coffee_list = []
    for coffe in range(len(file_coffees)):
        rezult_coffee = {}
        file_coordinates_coffee = file_coffees[coffe]['geoData']['coordinates']
        rezult_coffee['title'] = file_coffees[coffe]['Name']
        rezult_coffee['distance'] = distance.distance(coordinates_user, (
            file_coordinates_coffee[1],
            file_coordinates_coffee[0])
        ).km
        rezult_coffee['latitude'] = file_coordinates_coffee[1]
        rezult_coffee['longitude'] = file_coordinates_coffee[0]
        rezult_coffee_list.append(rezult_coffee)
    return rezult_coffee_list


def marker_map_coffe(sorted_distance, coordinates_user):
    m = folium.Map(
        location=[
            coordinates_user[0],
            coordinates_user[1],
        ],
        zoom_start=12,
        tiles="Stamen Terrain",
    )
    tooltip = "Я здесь!"
    folium.Marker(
        [
            coordinates_user[0],
            coordinates_user[1],
        ],
        popup=f'<i>Мое местоположение:"{address_user}"</i>',
        tooltip=tooltip,
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    for coffe in range(len(sorted_distance)):
        tooltip = sorted_distance[coffe]["title"]
        latitude, longitude = (
            sorted_distance[coffe]["latitude"],
            sorted_distance[coffe]["longitude"],
        )
        title_coffe = sorted_distance[coffe]["title"]
        public_phone = file_coffees[coffe]['PublicPhone'][0]['PublicPhone']
        folium.Marker(
            [
                latitude,
                longitude
            ],
            popup=f"<i>Название:{title_coffe}, Телефон:{public_phone}</i>",
            tooltip=tooltip,
            icon=folium.Icon(color="green")
        ).add_to(m)
    m.save("index.html")


if __name__ == '__main__':
    with open('coffee.json', 'r', encoding="CP1251") as my_file:
        file_content = my_file.read()
    file_coffees = json.loads(file_content)
    address_user = input('Где вы находитесь?')
    apikey = os.environ['apikey']
    coordinates_user = fetch_coordinates(apikey, address_user)
    sorted_distance = sorted(rezult_coffe_list(
        coordinates_user), key=get_coffe_dist)[:5]
    marker_map_coffe(sorted_distance, coordinates_user)
    app = Flask(__name__)
    app.add_url_rule('/', 'coffe map', coffee_map)
    app.run('0.0.0.0')
