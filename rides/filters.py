from django_filters import rest_framework as filters

from rides.models import Ride


class RideFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    rider_email = filters.CharFilter(field_name='id_rider__email', lookup_expr='exact')

    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
