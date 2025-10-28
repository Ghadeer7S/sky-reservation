from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'country', 'city']
    list_filter = ['country', 'city']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['user__first_name', 'user__last_name', 'phone_number']
