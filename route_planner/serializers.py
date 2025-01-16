from rest_framework import serializers


class GeoCoordinatesSerializer(serializers.Serializer):
    """Serializer for geographic coordinate system requests."""
    start_coords_lat = serializers.FloatField()
    start_coords_lon = serializers.FloatField()
    end_coords_lat = serializers.FloatField()
    end_coords_lon = serializers.FloatField()
