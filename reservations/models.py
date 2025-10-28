from django.contrib import admin
from django.db import models
from django.conf import settings
from flights.models import Flight
import string, random

class Reservation(models.Model):
    STATUS_PENDING = 'PN'
    STATUS_CONFIRMED = 'CF'
    STATUS_CANCELLED = 'CC'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='reservations')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')
    seats = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_PENDING)
    pnr_code = models.CharField(max_length=6, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.pnr_code})"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display()
    def flight_number(self):
        return self.flight.flight_number

    def generate_pnr(self):
        letters = string.ascii_uppercase
        return ''.join(random.choices(letters, k= 6))

    def save(self, *args, **kwargs):
        if not self.pnr_code:
            new_code = self.generate_pnr()
            while Reservation.objects.filter(pnr_code=new_code).exists():
                new_code = self.generate_pnr()
            self.pnr_code = new_code
        super().save(*args, **kwargs)


class Passenger(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'), 
        (GENDER_FEMALE, 'Female')
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='passengers')
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()

    def __str__(self):
        return f"Passenger {self.full_name} ({self.passport_number})"
    
    @admin.display(ordering='reservation__user__first_name')
    def Reservation(self):
        return f"{self.reservation.user.first_name} {self.reservation.flight.flight_number}"