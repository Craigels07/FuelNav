import openrouteservice
from openrouteservice import convert

client = openrouteservice.Client(key='5b3ce3597851110001cf6248d88442c89bd24f5dab0640dc81b5ce4d')
MAX_RANGE = 500 # maximum range of 500 miles
fuel_efficiency = 10 # miles per gallon

def get_route(start_coords, end_coords):
    """
    Get the route between two coordinates using OpenRouteService.
    Args:
        start_coords (tuple): (longitude, latitude) of the start point.
        end_coords (tuple): (longitude, latitude) of the end point.
    Returns:
        dict: The route and other related details.
    """
    routes = client.directions(
        coordinates=[start_coords, end_coords],
        profile='driving-car',
        format='geojson'
    )

    return routes

def get_distance(start_coords, end_coords):
    """
    Get the distance between two points using OpenRouteService.
    Args:
        start_coords (tuple): (longitude, latitude) of the start point.
        end_coords (tuple): (longitude, latitude) of the end point.
    Returns:
        float: The distance in kilometers.
    """
    route = get_route(start_coords, end_coords)
    distance = route['features'][0]['properties']['segments'][0]['distance'] / 1000  # in km
    return distance
