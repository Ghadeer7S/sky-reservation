from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Reservation
from flights.models import Flight

def validate_passenger_limit(reservation):
    if reservation.passengers.count() >= reservation.seats:
        raise ValidationError("❌ No more passengers can be added, all seats are booked.")

def validate_reservation_status_change(reservation, new_status):
    if new_status == Reservation.STATUS_CONFIRMED:
        raise ValidationError("You cannot confirm your reservation. Only admins can do that.")
    
def validate_passenger_can_be_modified(reservation):
    if reservation.status == Reservation.STATUS_CANCELLED:
        raise ValidationError("Cannot modify a cancelled reservation.")
    if reservation.status == Reservation.STATUS_CONFIRMED:
        raise ValidationError("Cannot modify confirmed reservation.")
    
def validate_flight_is_bookable(flight):
    if flight.status in [Flight.STATUS_CANCELLED, Flight.STATUS_COMPLETED]:
        raise ValidationError("Cannot create a reservation for a cancelled or completed flight.")
