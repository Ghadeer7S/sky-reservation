from rest_framework import serializers
from .models import Airline, Airplane
from flights.models import Flight, Airport
from core.validators import validate_flight

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'code', 'country', 'description']

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'registration_number', 'model', 'capacity']

    def create(self, validated_data):
        airline_id = self.context['airline_id']
        return Airplane.objects.create(airline_id=airline_id, **validated_data)
    
class CustomFlightSerializer(serializers.ModelSerializer):
    # read only fields
    airline = serializers.ReadOnlyField(source='airline.name')
    airplane = serializers.ReadOnlyField(source='airplane.registration_number')
    departure_airport = serializers.ReadOnlyField(source='departure_airport.code')
    arrival_airport = serializers.ReadOnlyField(source='arrival_airport.code')
    flight_number = serializers.ReadOnlyField()
    
    # write only fields
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.none(), write_only=True,
        label='Airplane'
    )
    arrival_airport_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Airport.objects.all(),
        write_only=True,
        label='Arrival airport'
    )
    departure_airport_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Airport.objects.all(),
        write_only=True,
        label='Departure airport'
    )
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        airline_id = self.context.get('airline_id')
        if airline_id:
            self.fields['airplane_id'].queryset = Airplane.objects.filter(airline_id=airline_id)

    class Meta:
        model = Flight
        fields = ['id', 'airline',
                  'airplane_id', 'airplane', 'flight_number',
                  'departure_airport','arrival_airport',
                  'departure_airport_code', 'arrival_airport_code',
                  'departure_time', 'arrival_time',
                  'status', 'price']

    def to_internal_value(self, data):
        ret =  super().to_internal_value(data)
        if 'arrival_airport_code' in ret:
            ret['arrival_airport'] = ret.pop('arrival_airport_code')
        
        if 'departure_airport_code' in ret:
            ret['departure_airport'] = ret.pop('departure_airport_code')

        if 'airplane_id' in ret:
            ret['airplane'] = ret.pop('airplane_id')
        
        return ret

    def validate(self, attrs):
        return validate_flight(attrs)

    def create(self, validated_data):
        airline_id = self.context['airline_id']
        return Flight.objects.create(airline_id=airline_id, **validated_data)
