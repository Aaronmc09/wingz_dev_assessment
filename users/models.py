from django.db import models


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin"
        DRIVER = "driver"
        RIDER = "rider"

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
