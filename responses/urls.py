from django.urls import path

from .apis import AddResponseView

app_name = "responses"

urlpatterns = [
    path("add", AddResponseView.as_view(), name="add-response-to-form"),
]
