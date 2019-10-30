from django.contrib import admin
from . import models


class BatchAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created_on', 'modified_by', 'modified_on',)
    ordering = ['created_by', 'created_on', 'modified_by', 'modified_on',]


class FileToBeDeletedAdmin(admin.ModelAdmin):
    list_display = ('batch', 'file', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['batch', 'file', ]
    raw_id_fields = ('file',)


class DeletedFileAdmin(admin.ModelAdmin):
    list_display = ('bucket', 'object_storage_key', 'filename', 'etag', 'size', 'source_file', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['bucket', 'object_storage_key', 'filename', 'etag', 'size', 'source_file', 'created_by', 'created_on', 'modified_by', 'modified_on', ]
    readonly_fields = ('sha1_unique_together', )


class MarkFilesDeleteCommandAdmin(admin.ModelAdmin):
    list_display = ('batch', 'command', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['batch', 'command', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


admin.site.register(models.FileToBeDeleted, FileToBeDeletedAdmin)
admin.site.register(models.Batch, BatchAdmin)
admin.site.register(models.DeletedFile, DeletedFileAdmin)
admin.site.register(models.MarkFilesDeleteCommand, MarkFilesDeleteCommandAdmin)
