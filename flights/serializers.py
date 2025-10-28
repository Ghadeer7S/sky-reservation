from rest_framework import serializers
from .models import Airport, Flight
from airlines.models import Airplane
from core.validators import validate_flight

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'country', 'city']

class CustomAirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['model', 'registration_number']

class FlightSerializer(serializers.ModelSerializer):
    # read only fields
    airline = serializers.ReadOnlyField(source='airline.name')
    airplane = CustomAirplaneSerializer(read_only=True)
    departure_airport = serializers.ReadOnlyField(source='departure_airport.__str__')
    arrival_airport = serializers.ReadOnlyField(source='arrival_airport.__str__')
    flight_number = serializers.ReadOnlyField()
    
    # write only fields
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(), write_only=True,
        label = 'Airplane'
    )
    arrival_airport_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Airport.objects.all(),
        write_only=True,
        label='Arrival airport'
    )
    
    
    class Meta:
        model = Flight
        fields = ['id', 'airline',
                  'airplane_id', 'airplane', 'flight_number',
                  'departure_airport','arrival_airport', 'arrival_airport_code',
                  'departure_time', 'arrival_time',
                  'status', 'price']
        

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if 'arrival_airport_code' in ret:
            ret['arrival_airport'] = ret.pop('arrival_airport_code')
        
        if 'airplane_id' in ret:
            ret['airplane'] = ret.pop('airplane_id')

        ret['departure_airport'] = self.context.get('departure_airport')

        return ret


    def validate(self, attrs):
        return validate_flight(attrs, instance=self.instance)
        

    def create(self, validated_data):
        return Flight.objects.create(
            **validated_data
        )
