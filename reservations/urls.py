from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('reservations', views.ReservationViewSet)
router.register('my/reservations', views.MyReservationViewSet, basename='my-reservations')

reservations_router = routers.NestedDefaultRouter(router, 'reservations', lookup='reservation')
reservations_router.register('passengers', views.PassengerViewSet, basename='reservation-passengers')

my_reservations_router = routers.NestedDefaultRouter(router, 'my/reservations', lookup='my_reservation')
my_reservations_router.register('passengers', views.MyPassengerViewSet, basename='my-reservation-passengers')

urlpatterns = router.urls + reservations_router.urls + my_reservations_router.urls