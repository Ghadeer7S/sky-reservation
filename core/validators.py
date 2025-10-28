from rest_framework.exceptions import ValidationError
from flights.models import Flight

def validate_flight(attrs, instance=None):
    errors = {}

    departure_airport = attrs.get('departure_airport')
    arrival_airport = attrs.get('arrival_airport')

    departure_time = attrs.get('departure_time')
    arrival_time = attrs.get('arrival_time')
    
    airplane = attrs.get('airplane')

    if departure_airport and arrival_airport and departure_airport == arrival_airport:
        errors['invalid_route'] = 'Departure and arrival airports must be different.'

    if departure_time and arrival_time and arrival_time <= departure_time:
        errors['schedule'] = 'Arrival time must be after departure time.'

    if airplane:
        overlapping = Flight.objects.filter(
            airplane=airplane,
            departure_time__lt=arrival_time,
            arrival_time__gt=departure_time
        )
        
        if instance:
            overlapping = overlapping.exclude(id=instance.id)

        if overlapping.exists():
            errors['airplane'] = 'This airplane is already assigned to another flight in this time.'

    if errors:
        raise ValidationError(errors)

    return attrs
