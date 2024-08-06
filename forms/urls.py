from django.urls import include, path

app_name = "forms"

form_urls = [
    # path("add/<int:form_id>/", AddField.as_view(), name="add-field-to-form"),
]

field_urls = [
    # path("add/<int:form_id>/", AddForm.as_view(), name="add-field-to-form"),
]

pipline_urls = [
    # path("add/"),
]

urlpatterns = [
    path("", include(form_urls)),
    path("fields/", include(field_urls)),
    path("piplines/", include(pipline_urls)),
]
