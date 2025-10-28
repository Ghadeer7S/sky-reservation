from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import AirportSerializer, FlightSerializer
from .models import Airport, Flight

IsAdminOrReadOnly = import_string(settings.CUSTOM_PERMISSIONS['IS_ADMIN_OR_READ_ONLY'])

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def departures(self, request, pk=None):
        airport = self.get_object()
        flights = Flight.objects.select_related('airplane', 'departure_airport', 'arrival_airport'). \
                        filter(departure_airport=airport).order_by('departure_time')
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def arrivals(self, request, pk=None):
        airport = self.get_object()
        flights = Flight.objects.select_related('airplane', 'departure_airport', 'arrival_airport').\
                        filter(arrival_airport=airport).order_by('arrival_time')
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Flight.objects.select_related(
            'airline', 'airplane', 'departure_airport', 'arrival_airport') 
        airport_id = self.kwargs.get('airport_pk')
        return qs.filter(departure_airport=airport_id)
    
    def get_serializer_context(self):
        if not hasattr(self, '_departure_airport'):
            airport_id = self.kwargs.get('airport_pk')
            self._departure_airport = Airport.objects.only('id', 'code', 'city').get(id=airport_id)
        return{'departure_airport': self._departure_airport}