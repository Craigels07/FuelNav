import requests
import time
from route_planner.models import Truckstop
import urllib.parse

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def fetch_coordinates_from_api(url):
    """Fetch latitude and longitude from the Nominatim API."""
    headers = {
        "User-Agent": "MyAppName/1.0 (your.email@example.com)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None, None

def get_coordinates(name, city, state, country="US"):
    """Try to get coordinates first using the name, then fallback to the full address."""
    # Try using just the name of TruckStop first.
    encoded_name = urllib.parse.quote(name)
    name_url = f"https://nominatim.openstreetmap.org/search?q={encoded_name}&format=json"
    lat, lon = fetch_coordinates_from_api(name_url)

    if lat and lon:
        return lat, lon

    time.sleep(1) # if this was for work i would never add a hardcoded sleep here

    # If no coordinates were found, fallback to the full address :(
    print(f"Name search failed for: {name}. Trying full address search...")
    full_address = f"{city}, {state}, {country}"
    full_address_url = f"https://nominatim.openstreetmap.org/search?q={full_address}&format=json"
    return fetch_coordinates_from_api(full_address_url)



def populate_truck_stop_coordinates():
    truck_stops = Truckstop.objects.filter(latitude__isnull=True, longitude__isnull=True)
    for truck_stop in truck_stops:
        print(f"Processing Truckstop: {truck_stop.name}")
        lat, lon = get_coordinates(truck_stop.name, truck_stop.city, truck_stop.state, "US")
        time.sleep(1) # if this was for work i would never add a hardcoded sleep here
        if lat and lon:
            print(f"Found coordinates for {truck_stop.name}: {lat}, {lon}")
            truck_stop.latitude = lat
            truck_stop.longitude = lon
            truck_stop.save()
