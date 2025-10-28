from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('airlines', views.AirlineViewSet)

airlines_router = routers.NestedDefaultRouter(router, 'airlines', lookup='airline')
airlines_router.register('airplanes', views.AirplaneViewSet, basename='airline-airplanes')
airlines_router.register('flights', views.FlightAirlineViewSet, basename='airline-flights')

urlpatterns = router.urls + airlines_router.urls