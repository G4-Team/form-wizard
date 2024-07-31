import zoneinfo

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser):
    class Meta:
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["phone"], name="phone_idx"),
        ]

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

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class OtpVerificationCode(models.Model):
    phone = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now_time = timezone.datetime.now(tz=zoneinfo.ZoneInfo("Asia/Tehran"))
        if (now_time - self.created_at).total_seconds() > 120:
            return False
        return True
