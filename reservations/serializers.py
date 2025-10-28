from rest_framework import serializers
from core.models import User
from flights.models import Flight
from .models import Reservation, Passenger
from .validators import validate_passenger_limit, validate_flight_is_bookable

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), write_only=True)

    username = serializers.CharField(source='user.username', read_only=True)
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'username',
                 'flight_number', 'flight', 'seats', 'status',
                 'pnr_code', 'created_at', 'updated_at']

class MyReservationSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), write_only=True)

    username = serializers.CharField(source='user.username', read_only=True)
    flight_number = serializers.CharField(source='flight.flight_number', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'username',
                 'flight_number', 'flight', 'seats', 'status',
                 'pnr_code', 'created_at', 'updated_at']
        read_only_fields = ['status', 'pnr_code', 'created_at', 'updated_at']

    def validate(self, attrs):
        flight = attrs.get("flight")
        if flight:
            validate_flight_is_bookable(flight)
        return attrs

class PassengerSerializer(serializers.ModelSerializer):
    reservation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Passenger
        fields = ['id', 'full_name', 'passport_number',
                 'nationality', 'gender', 'birth_date', 'reservation']
    
    def validate(self, attrs):
        reservation_id = self.context.get('reservation_id')
        reservation = Reservation.objects.get(id=reservation_id)
        
        validate_passenger_limit(reservation)
        return attrs
    
    def create(self, validated_data):
        reservation_id = self.context['reservation_id']
        return Passenger.objects.create(reservation_id=reservation_id, **validated_data)