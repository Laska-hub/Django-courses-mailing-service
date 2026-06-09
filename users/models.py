from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)

    verification_token = models.UUIDField(default=uuid.uuid4, unique=True)

    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username

