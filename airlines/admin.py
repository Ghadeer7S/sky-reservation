from django.contrib import admin
from .models import Airline, Airplane

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country']
    list_filter = ['country']
    search_fields = ['name', 'code', 'country']

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ['model', 'airline', 'registration_number', 'capacity']
    list_filter = ['airline', 'model']
    search_fields = ['registration_number', 'model', 'capacity']