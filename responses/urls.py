from django.urls import path

from .apis import AddResponseView, ResponseRetriveApi, UpdateResponseView

app_name = "responses"

urlpatterns = [
    path("add", AddResponseView.as_view(), name="add-response-to-form"),
    path(
        "update/<int:response_id>", UpdateResponseView.as_view(), name="update-response"
    ),
    path(
        "list/<int:pipeline_sunbmission_id>",
        ResponseRetriveApi.as_view(),
        name="retrive-response",
    ),
]
