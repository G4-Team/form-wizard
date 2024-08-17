from django.contrib import admin

from .models import Category, Field, Form, Pipeline


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "id")


admin.site.register(Field)
admin.site.register(Form)

admin.site.register(Category)
