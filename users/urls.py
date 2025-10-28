from rest_framework_nested import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]   