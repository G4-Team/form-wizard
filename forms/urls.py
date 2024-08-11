from django.urls import include, path

from forms import views

app_name = "forms"

form_urls = [
    path("", views.FormListView.as_view(), name="form-list"),
    path("<int:form_id>", views.FormDataView.as_view(), name="form-data"),
    path("add", views.FormCreateView.as_view(), name="form-add"),
    path("update/<int:form_id>", views.FormUpdateView.as_view(), name="form-update"),
    path("delete/<int:form_id>", views.FormDeleteView.as_view(), name="form-delete"),
]

field_urls = [
    path("", views.FieldListView.as_view(), name="field-list"),
    path("<int:field_id>", views.FieldDataView.as_view(), name="field-data"),
    path("add", views.FieldCreateView.as_view(), name="field-add"),
    path("update/<int:field_id>", views.FieldUpdateView.as_view(), name="field-update"),
    path("delete/<int:field_id>", views.FieldDeleteView.as_view(), name="field-delete"),
    path("common-regex", views.CommonRegexApi.as_view(), name="list-common-regex"),
]

pipline_urls = [
    path("", views.PipelineListView.as_view(), name="pipeline-list"),
    path("<int:pipeline_id>", views.PipelineDataView.as_view(), name="pipeline-data"),
    path("add", views.PipelineCreateView.as_view(), name="pipeline-add"),
    path(
        "update/<int:pipeline_id>",
        views.PipelineUpdateView.as_view(),
        name="pipeline-update",
    ),
    path(
        "delete/<int:pipeline_id>",
        views.PipelineDeleteView.as_view(),
        name="pipeline-delete",
    ),
]

urlpatterns = [
    path("", include(form_urls)),
    path("fields/", include(field_urls)),
    path("pipelines/", include(pipline_urls)),
]
