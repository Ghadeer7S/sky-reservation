from django.contrib import admin
from .models import Reservation, Passenger

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'flight_number','seats', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_select_related = ['user', 'flight']
    search_fields = ['first_name', 'flight_number']


class ReservationListFilter(admin.SimpleListFilter):
    title = 'reservation'
    parameter_name = 'reservation'

    def lookups(self, request, model_admin):
        reservations = Reservation.objects.select_related('user', 'flight')
        return[
            (r.id, f"{r.user.first_name} {r.flight.flight_number}")
            for r in reservations
        ]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reservation__id=self.value())
        return queryset

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'passport_number', 'Reservation',  'gender', 'nationality']
    list_filter = ['gender', 'nationality', ReservationListFilter]
    list_select_related = ['reservation__user', 'reservation__flight']
    search_fields = ['full_name', 'passport_number']