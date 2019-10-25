from django.contrib import admin
from . import models


class FileToBeDeletedAdmin(admin.ModelAdmin):
    list_display = ('batch', 'file', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['batch', 'file', ]


admin.site.register(models.FileToBeDeleted, FileToBeDeletedAdmin)
