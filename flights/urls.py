from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('airports', views.AirportViewSet)

airports_router = routers.NestedDefaultRouter(router, 'airports', lookup='airport')
airports_router.register('flights', views.FlightViewSet, basename='airport-flights')

urlpatterns = router.urls + airports_router.urls