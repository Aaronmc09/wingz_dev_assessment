from django.db import models

from users.models import User


class Ride(models.Model):
    class Status(models.TextChoices):
        EN_ROUTE = "en-route"
        PICKUP = "pickup"
        DROPOFF = "dropoff"

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=Status.choices, db_index=True)
    id_rider = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rides_as_rider')
    id_driver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rides_as_driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"Ride {self.id_ride} - {self.status}"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='events', db_column='id_ride')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"RideEvent {self.id_ride_event} - {self.description}"
