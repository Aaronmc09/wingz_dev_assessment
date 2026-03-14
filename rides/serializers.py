from rest_framework import serializers

from rides.models import Ride, RideEvent
from users.serializers import UserReadSerializer


class RideEventReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'


class RideEventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride', 'description', 'created_at']


class RideReadSerializer(serializers.ModelSerializer):
    id_rider = UserReadSerializer()
    id_driver = UserReadSerializer()
    events = RideEventReadSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        fields = '__all__'


class RideWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
        ]
