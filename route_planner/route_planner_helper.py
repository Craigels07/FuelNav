env_variables = '5b3ce3597851110001cf6248d88442c89bd24f5dab0640dc81b5ce4d'
import openrouteservice
from route_planner.models import Truckstop
from math import radians, sin, cos, sqrt, atan2
from scipy.spatial import KDTree
import numpy as np
import haversine as hs
from haversine import Unit


MAX_RANGE = 500 # maximum driveable range of 500 miles
FUEL_EFFICIENCY = 10 # assuming 10 miles per gallon
SEARCH_RADIUS = 15

def get_route(start_coords, end_coords):
    """
    Get the route between two coordinates using OpenRouteService.
    Args:
        start_coords (tuple): (longitude, latitude) of the start point.
        end_coords (tuple): (longitude, latitude) of the end point.
    Returns:
        dict: The route and other related details.
    """
    client = openrouteservice.Client(key=env_variables)
    routes = client.directions(
        coordinates=[start_coords, end_coords],
        profile='driving-car',
        format='geojson',
    )

    return routes

def get_distance(route):
    """
    Get the distance between two points using OpenRouteService.
    Args:
        start_coords (tuple): (longitude, latitude) of the start point.
        end_coords (tuple): (longitude, latitude) of the end point.
    Returns:
        float: The distance in kilometers.
    """

    total_distance_meters = route["features"][0]["properties"]["summary"]["distance"]
    total_distance_miles = total_distance_meters / 1609.34
    return total_distance_miles

def haversine(coord1, coord2):
    """Haversine formula to calculate distance between two points."""
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    R = 3958.8
    return R * c  # Distance in miles

def get_nearby_truckstops():
    """Fetch all truck stops and build a KDTree for fast lookup."""

    truck_stops = list(Truckstop.objects.all())
    stop_coords = np.array([(ts.longitude, ts.latitude) for ts in truck_stops])

    return truck_stops, KDTree(stop_coords)

def extract_segment_waypoints(route):
    """Extracts waypoints from segment steps to reduce route complexity."""
    waypoints = set()
    segments = route["features"][0]["properties"]["segments"]

    for segment in segments:
        for step in segment["steps"]:
            waypoints.update(step["way_points"])

    return sorted(waypoints)


def optimize_segments(route):

    segment_waypoints = extract_segment_waypoints(route)
    print("Extracted waypoints:", segment_waypoints)
    route_coords  = route["features"][0]["geometry"]["coordinates"]
    reduced_route_coords = [route_coords[i] for i in segment_waypoints]

    truck_stops, tree = get_nearby_truckstops()
    if not truck_stops:
        print("No truck stops found along the route.")
        return None

    total_distance_travelled = 0
    current_pos = reduced_route_coords[0]
    remaining_range = MAX_RANGE
    fuel_stops = []
    extra_fuelstop_travel_distance = 0
    total_fuel_cost = 0

    for next_pos in reduced_route_coords[1:]:
        distance_to_next_coordinate = haversine(current_pos, next_pos)

        total_distance_travelled += distance_to_next_coordinate
        remaining_range -= distance_to_next_coordinate

        if remaining_range <= SEARCH_RADIUS: # Stop before running out of fuel!

            distance_to_nearest_truckstop, index = tree.query(next_pos)
            nearest_stop = truck_stops[index]
            nearest_stop_geo = [nearest_stop.latitude, nearest_stop.longitude]
            extra_fuelstop_travel_distance += haversine(current_pos, nearest_stop_geo)

            fuel_needed = min((MAX_RANGE - remaining_range) / FUEL_EFFICIENCY, MAX_RANGE/FUEL_EFFICIENCY)

            total_cost = fuel_needed * nearest_stop.retail_price
            total_fuel_cost += total_cost
            fuel_stops.append({
                "name": nearest_stop.name,
                "location": [nearest_stop.latitude, nearest_stop.longitude],
                "price": nearest_stop.retail_price,
                "fuel_needed": fuel_needed,
                "total_cost": total_cost
            })

            remaining_range = MAX_RANGE

        current_pos = next_pos
    extra_fuelstop_travel_distance = extra_fuelstop_travel_distance/1609
    print("extra_fuelstop_travel_distance: ", extra_fuelstop_travel_distance)
    print("Reduced Route Distance:", total_distance_travelled)
    return fuel_stops, extra_fuelstop_travel_distance, total_fuel_cost





