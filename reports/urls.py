from django.urls import path

from .apis import PeriodicReportApi

app_name = "reports"

urlpatterns = [
    path(
        "periodic/<int:pipeline_id>/",
        PeriodicReportApi.as_view(),
        name="periodic-report",
    ),
]
