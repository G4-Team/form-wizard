from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apis import ProfileApi, RegisterUserApi

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterUserApi.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileApi.as_view(), name="profile"),
]
