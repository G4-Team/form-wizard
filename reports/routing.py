from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/form-reports/<int:pipeline_id>/", consumers.FormReportConsumer.as_asgi()),
]
