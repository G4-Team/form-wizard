from django.contrib import admin

from .models import Category, Field, Form, Pipeline

admin.site.register(Field)
admin.site.register(Form)
admin.site.register(Pipeline)
admin.site.register(Category)
