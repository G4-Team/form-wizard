from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apis import ProfileApi, RegisterUserApi, SendOtpCodeApi, ValidateOtpCodeApi

app_name = "accounts"
otp_urls = [
    path("send/", SendOtpCodeApi.as_view(), name="send-otp-code"),
    path("validate/", ValidateOtpCodeApi.as_view(), name="validateotp-code"),
]
urlpatterns = [
    path("register/", RegisterUserApi.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileApi.as_view(), name="profile"),
    path("otp/", include(otp_urls)),
]
