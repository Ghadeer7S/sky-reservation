from rest_framework.exceptions import PermissionDenied
from .models import Reservation
from rest_framework import permissions

class IsOwnerOfReservation(permissions.BasePermission):
    def has_permission(self, request, view):
        reservation_id = view.kwargs.get('my_reservation_pk')
        if reservation_id is None:
            return True

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise PermissionDenied("Reservation not found.")

        if reservation.user != request.user:
            raise PermissionDenied("You do not own this reservation.")

        view.reservation = reservation
        return True


class CanAccessOrModifyPassenger(permissions.BasePermission):
    def has_permission(self, request, view):
        reservation_id = view.kwargs.get('my_reservation_pk')
        if not reservation_id:
            return True

        if hasattr(view, "reservation"):
            reservation = view.reservation
        else:
            try:
                reservation = Reservation.objects.get(id=reservation_id)
            except Reservation.DoesNotExist:
                raise PermissionDenied("Reservation not found.")
            view.reservation = reservation

        if request.method in permissions.SAFE_METHODS:
            return True

        if reservation.status in [Reservation.STATUS_CANCELLED, Reservation.STATUS_CONFIRMED]:
            raise PermissionDenied("Cannot modify passengers for a cancelled or confirmed reservation.")

        return True
