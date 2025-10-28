from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.name}"
    
class Airplane(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    registration_number = models.CharField(max_length=255, unique=True)
    model = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.model} - {self.registration_number}"
    