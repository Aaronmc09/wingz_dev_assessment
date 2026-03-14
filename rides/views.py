from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Ride
from .serializers import RideReadSerializer, RideWriteSerializer


class RideViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(id_rider=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RideWriteSerializer
        return RideReadSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
        }


