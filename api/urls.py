from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("forms/", include("forms.urls", namespace="forms")),
    path("responses/", include("responses.urls", namespace="responses")),
    path("reports/", include("reports.urls", namespace="reports")),
]
