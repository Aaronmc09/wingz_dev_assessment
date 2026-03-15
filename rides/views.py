from django.db.models import F, FloatField, ExpressionWrapper, Prefetch
from django.db.models.functions import Power
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from rides.filters import RideFilter
from rides.models import Ride, RideEvent
from rides.permissions import IsAdminUser
from rides.serializers import (
    RideReadSerializer,
    RideWriteSerializer,
    RideEventReadSerializer,
    RideEventWriteSerializer,
)

DISTANCE_BOUNDING_BOX_DEGREES = 0.5


class RideViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = [IsAdminUser]
    filterset_class = RideFilter

    def get_queryset(self):
        now = timezone.now()
        last_24h = now - timezone.timedelta(hours=24)

        queryset = Ride.objects.select_related(
            'id_rider', 'id_driver'
        ).prefetch_related(
            Prefetch(
                'events',
                queryset=RideEvent.objects.filter(created_at__gte=last_24h),
                to_attr='todays_ride_events',
            )
        )

        # Sorting
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'pickup_time':
            order = self.request.query_params.get('order', 'asc')
            prefix = '-' if order == 'desc' else ''
            queryset = queryset.order_by(f'{prefix}pickup_time')
        elif sort_by == 'distance':
            lat = self.request.query_params.get('latitude')
            lon = self.request.query_params.get('longitude')
            if not lat or not lon:
                raise ValidationError(
                    {'detail': 'latitude and longitude are required when sorting by distance.'}
                )
            try:
                lat = float(lat)
                lon = float(lon)
            except (TypeError, ValueError):
                raise ValidationError(
                    {'detail': 'latitude and longitude must be valid numbers.'}
                )
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValidationError(
                    {'detail': 'latitude must be between -90 and 90, longitude between -180 and 180.'}
                )

            bb = DISTANCE_BOUNDING_BOX_DEGREES
            queryset = queryset.filter(
                pickup_latitude__range=(lat - bb, lat + bb),
                pickup_longitude__range=(lon - bb, lon + bb),
            )
            distance = ExpressionWrapper(
                Power(F('pickup_latitude') - lat, 2)
                + Power(F('pickup_longitude') - lon, 2),
                output_field=FloatField(),
            )
            queryset = queryset.annotate(distance=distance).order_by('distance')

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RideWriteSerializer
        return RideReadSerializer
