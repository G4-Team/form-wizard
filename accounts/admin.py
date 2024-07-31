from django.contrib import admin

from .models import OtpVerificationCode, User

admin.site.register(User)
admin.site.register(OtpVerificationCode)
