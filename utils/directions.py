import math

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_direction_png(direction):
    print(direction)
    directions_pngs_mapping = {
        "N": "/static/directions/arrow_north.png",
        "NE": "/static/directions/arrow_north_east.png",
        "NW": "/static/directions/arrow_north_west.png",
        "E": "/static/directions/arrow_east.png",
        "S": "/static/directions/arrow_south.png",
        "SE": "/static/directions/arrow_south_east.png",
        "SW": "/static/directions/arrow_south_west.png",
        "W": "/static/directions/arrow_west.png",
    }
    return directions_pngs_mapping.get(direction)

def get_coordinates(country_name):
    # Add checks here to see if the lat and long are
    # properly returned (maybe a timeout as well)
    geolocator = Nominatim(user_agent="GuessFlag")
    location = geolocator.geocode(country_name)
    return (location.latitude, location.longitude)

def calculate_distance(coords1, coords2):
    distance = geodesic(coords1, coords2).kilometers
    return distance


def calculate_direction(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1
    angle = math.atan2(math.sin(delta_lon), math.cos(lat1) * math.tan(lat2) - math.sin(lat1) * math.cos(delta_lon))
    angle = math.degrees(angle)
    angle = (angle + 360) % 360
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(angle / 45) % 8

    return directions[index]