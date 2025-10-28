from django.contrib import admin
from .models import Airport, Flight

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'city']
    list_filter = ['country', 'city']
    search_fields = ['name', 'code']

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['airplane', 'departure_airport', 'arrival_airport', 'flight_number',
                     'departure_time', 'arrival_time', 'price', 'status']
    list_filter = ['airplane', 'status']
    search_fields = ['flight_number']