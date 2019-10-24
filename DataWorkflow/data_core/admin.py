from django.contrib import admin
import data_core.models


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['name', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class BucketAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'endpoint', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['friendly_name', 'name', 'endpoint', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class FileAdmin(admin.ModelAdmin):
    list_display = ('bucket', 'object_storage_key', 'etag', 'size', 'source_file', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['bucket', 'object_storage_key', 'etag', 'size', 'source_file', 'created_by', 'created_on', 'modified_by', 'modified_on', ]
    readonly_fields = ('sha1_unique_together', )


class SourceFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_on', 'modified_by', 'modified_on', )
    ordering = ['name', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


admin.site.register(data_core.models.Endpoint, EndpointAdmin)
admin.site.register(data_core.models.Bucket, BucketAdmin)
admin.site.register(data_core.models.File, FileAdmin)
admin.site.register(data_core.models.SourceFile, SourceFileAdmin)
