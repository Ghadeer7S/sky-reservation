from rest_framework import viewsets
from django.conf import settings
from django.utils.module_loading import import_string
from .serializers import AirplaneSerializer, AirlineSerializer, CustomFlightSerializer
from .models import Airline, Airplane
from flights.models import Flight

IsAdminOrReadOnly = import_string(settings.CUSTOM_PERMISSIONS['IS_ADMIN_OR_READ_ONLY'])

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly]

class AirplaneViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Airplane.objects.filter(airline_id=self.kwargs['airline_pk'])

    def get_serializer_context(self):
        return {'airline_id': self.kwargs['airline_pk']}
    
class FlightAirlineViewSet(viewsets.ModelViewSet):
    serializer_class = CustomFlightSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Flight.objects.\
            select_related('airline', 'airplane', 'departure_airport', 'arrival_airport').\
                filter(airline_id=self.kwargs['airline_pk'])

    def get_serializer_context(self):
        return {'airline_id': self.kwargs['airline_pk']}