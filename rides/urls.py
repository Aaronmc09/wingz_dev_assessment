from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RideViewSet

rides_router = DefaultRouter()
rides_router.register(r'', RideViewSet, basename='rides')

urls = [
    path('', rides_router.urls),
]