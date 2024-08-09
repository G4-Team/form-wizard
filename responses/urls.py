from django.urls import path

from .apis import AddResponseView, UpdateResponseView

app_name = "responses"

urlpatterns = [
    path("add", AddResponseView.as_view(), name="add-response-to-form"),
    path(
        "update/<int:response_id>", UpdateResponseView.as_view(), name="update-response"
    ),
]
