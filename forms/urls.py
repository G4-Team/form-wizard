from django.urls import include, path

from rest_framework import routers

from forms import views
from forms.views import FormAddField

app_name = "forms"

form_urls = [
    path('', views.FormListView.as_view(),name='form-list'),
    path('all/', views.AllFormListView.as_view(), name='all-form-list'),
    path('add/', views.FormCreateView.as_view(),name='form-add'),
    path('<int:pk>/', views.FormDataView.as_view(), name='form-data'),
    path("update/<int:form_id>/", FormAddField.as_view(), name="add-field-to-form"),
    path('delete/<int:pk>/', views.FormDeleteView.as_view(), name='form-delete'),
]

field_urls = [
    path('', views.FieldListView.as_view(), name='field-list'),
    path('all/', views.AllFieldListView.as_view(), name='all-field-list'),
    path('add/', views.FieldCreateView.as_view(), name='field-add'),
    path('<int:pk>/', views.FieldDataView.as_view(), name='field-data'),
    path('update/<int:pk>/', views.FieldUpdateView.as_view(), name='field-update'),
    path('delete/<int:pk>/', views.FieldDeleteView.as_view(), name='field-delete'),
]

pipline_urls = [
    # path("add/"),
]

urlpatterns = [
    path("", include(form_urls)),
    path("fields/", include(field_urls)),
    path("piplines/", include(pipline_urls)),
]
