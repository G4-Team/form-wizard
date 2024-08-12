from django.urls import path

from .apis import PeriodicReportApi, SubsrcribeReportApi

app_name = "reports"

urlpatterns = [
    path(
        "periodic/<int:pipeline_id>/",
        PeriodicReportApi.as_view(),
        name="periodic-report",
    ),
    path(
        "subscribe/<int:pipeline_id>/",
        SubsrcribeReportApi.as_view(),
        name="subscribe-for-report",
    ),
]
