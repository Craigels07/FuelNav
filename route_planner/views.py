from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GeoCoordinatesSerializer
from .route_planner_helper import get_route, get_distance, optimize_segments
from django.shortcuts import render
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="fuel_nav")
class RoutePlannerView(APIView):
    """Route planner view to return a map."""
    serializer_class = GeoCoordinatesSerializer

    def get(self, request):
        start_coords_lat = request.GET.get('start_coords_lat')
        start_coords_lon = request.GET.get('start_coords_lon')
        end_coords_lat = request.GET.get('end_coords_lat')
        end_coords_lon = request.GET.get('end_coords_lon')

        if start_coords_lat and start_coords_lon and end_coords_lat and end_coords_lon:
            start_coords = (float(start_coords_lon), float(start_coords_lat))
            end_coords = (float(end_coords_lon), float(end_coords_lat))

        route = get_route(start_coords, end_coords) # should be lat, long but switched for it to work.
        total_distance_miles = get_distance(route)

        fuelStops, extra_fuelstop_travel_distance, total_fuel_cost = optimize_segments(route)
        total_distance_with_fuel_stops = extra_fuelstop_travel_distance + total_distance_miles
        print(fuelStops)

        print(f"Total distance: {total_distance_miles:.2f} miles")

        context = {
            'route': route,
            'distance': total_distance_miles,
            'total_distance_with_fuel_stops': total_distance_with_fuel_stops,
            'start_coords': {'lat': start_coords_lat, 'lon': start_coords_lon},
            'end_coords': {'lat': end_coords_lat, 'lon': end_coords_lon},
            'fuelStops': fuelStops,
            'total_fuel_cost': total_fuel_cost
        }
        return render(request, 'route_planner/show_route.html', context)

