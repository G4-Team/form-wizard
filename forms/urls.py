from django.urls import include, path

from rest_framework import routers

from forms import views
from forms.views import FormAddField

app_name = "forms"

form_urls = [
    path('', views.FormListView.as_view(),name='form-list'),
    path('add/', views.FormCreateView.as_view(),name='form-add'),
    path("<int:form_id>/add/<int:field_id>/", FormAddField.as_view(), name="add-field-to-form"),
]

field_urls = [
    path('', views.FieldListView.as_view(), name='field-list'),
    path('all/', views.AllFieldListView.as_view(), name='all-field-list'),
    path('add/', views.FieldCreateView.as_view(), name='field-add'),
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

router = routers.SimpleRouter()
router.register('forms', views.FormViewSet)
urlpatterns += router.urls
