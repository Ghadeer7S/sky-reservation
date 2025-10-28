from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import ReservationSerializer, PassengerSerializer, MyReservationSerializer
from .models import Reservation, Passenger
from .permissions import CanAccessOrModifyPassenger, IsOwnerOfReservation
from .validators import validate_passenger_can_be_modified

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('user', 'flight').all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]

class MyReservationViewSet(viewsets.ModelViewSet):
    serializer_class = MyReservationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfReservation]

    def get_queryset(self):
        return Reservation.objects.select_related('user', 'flight').filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, pk=None):
        reservation = self.get_object()

        validate_passenger_can_be_modified(reservation)

        serializer = MyReservationSerializer(reservation, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = Reservation.STATUS_CANCELLED
        reservation.save()

        return Response(
            {"detail": "Reservation cancelled successfully"},
            status=status.HTTP_200_OK
        )    

class PassengerViewSet(viewsets.ModelViewSet):
    serializer_class = PassengerSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Passenger.objects.\
            select_related('reservation__user', 'reservation__flight')\
                .filter(reservation_id=self.kwargs['reservation_pk'])
    
    def get_serializer_context(self):
        return {'reservation_id': self.kwargs['reservation_pk']}
    
class MyPassengerViewSet(viewsets.ModelViewSet):
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated, CanAccessOrModifyPassenger]

    def get_queryset(self):
        return Passenger.objects.\
                select_related(
                    'reservation__user', 'reservation__flight')\
                            .filter(reservation_id=self.kwargs['my_reservation_pk'])
    
    def get_serializer_context(self):
        return {'reservation_id': self.kwargs['my_reservation_pk']}