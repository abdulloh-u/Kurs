from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True, verbose_name="Telefon raqami")
    is_verified = models.BooleanField(default=False, verbose_name="Tasdiqlangan")

    def __str__(self):
        return f"{self.username} ({self.phone_number})"