from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=250, unique=True)
    phone = models.CharField(max_length=11, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "phone",
        "first_name",
        "last_name",
    ]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email
