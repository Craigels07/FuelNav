from django.contrib import admin
from .models import Truckstop

@admin.register(Truckstop)
class TruckstopAdmin(admin.ModelAdmin):
    list_display = ('opis_id', 'name', 'address', 'city', 'state', 'rack_id', 'retail_price', 'latitude', 'longitude')
    search_fields = ('opis_id', 'name', 'city')
    list_filter = ('state',)
    ordering = ('opis_id',)
