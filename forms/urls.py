from django.urls import include, path

from forms import views

app_name = "forms"

form_urls = [
    # path("add/<int:form_id>/", AddField.as_view(), name="add-field-to-form"),
]

field_urls = [
    path('fields/', views.FieldListView.as_view(), name='field-list'),
    path('field/add/', views.FieldCreateView.as_view(), name='field-add'),
    path('field/update/<int:pk>/', views.FieldUpdateView.as_view(), name='field-update'),
    path('field/delete/<int:pk>/', views.FieldDeleteView.as_view(), name='field-delete'),
]

pipline_urls = [
    # path("add/"),
]

urlpatterns = [
    path("", include(form_urls)),
    path("fields/", include(field_urls)),
    path("piplines/", include(pipline_urls)),
]
