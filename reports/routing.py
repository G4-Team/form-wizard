from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/form-reports/", consumers.FormReportConsumer.as_asgi()),
]
