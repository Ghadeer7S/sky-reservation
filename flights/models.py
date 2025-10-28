from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from airlines.models import Airline, Airplane

class Airport(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.code}"
    
class Flight(models.Model):
    STATUS_SCHEDULED = 'SC'
    STATUS_DELAYED = 'DL'
    STATUS_CANCELLED = 'CC'
    STATUS_COMPLETED = 'CM'

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_DELAYED, 'Delayed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed')
    ]

    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    flight_number = models.CharField(max_length=255, unique=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default= STATUS_SCHEDULED)

    def save(self, *args, **kwargs):
        if self.airplane:
            self.airline = self.airplane.airline

        if not self.flight_number:
            airline_code = self.airline.code if self.airline else "XX"
            unique_code = get_random_string(4, allowed_chars='1234567890')
            self.flight_number = f"{airline_code}{unique_code}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.flight_number}"
    
