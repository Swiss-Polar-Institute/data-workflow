from django.contrib import admin
import publications.models


# Register your models here.
class IdentifierTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('uri', 'type', )
    ordering = ['uri', 'type', ]


class ResourceTypeGeneralAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'type_general', )
    ordering = ['description', 'type_general', ]


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'publisher', 'publication_year', 'resource_type', 'version', )
    ordering = ['identifier', 'publisher', 'publication_year', 'resource_type', 'version', ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ('publication', 'size', )
    ordering = ['publication', 'size', ]


class FormatAdmin(admin.ModelAdmin):
    list_display = ('publication', 'format', )
    ordering = ['publication', 'format', ]


class RightsAdmin(admin.ModelAdmin):
    list_display = ('publication', 'statement', 'uri', 'identifier', 'identifier_scheme', 'scheme_uri', )
    ordering = ['publication', 'statement', 'uri', 'identifier', 'identifier_scheme', 'scheme_uri', ]


class FunderIdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'type', 'scheme_uri', )
    ordering = ['identifier', 'type', 'scheme_uri', ]


class AwardAdmin(admin.ModelAdmin):
    list_display = ('number', 'uri', )
    ordering = ['number', 'uri', ]


class FundingReferenceAdmin(admin.ModelAdmin):
    list_display = ('publication', 'funder_name', 'funder_identifier', 'award_number', 'award_title', )
    ordering = ['publication', 'funder_name', 'funder_identifier', 'award_number', 'award_title', ]


class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class RelatedIdentifierTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class RelatedIdentifierAdmin(admin.ModelAdmin):
    list_display = ('publication', 'identifier', 'related_identifier_type', 'relation_type', )
    ordering = ['publication', 'identifier', 'related_identifier_type', 'relation_type', ]


class DateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class DateAdmin(admin.ModelAdmin):
    list_display = ('publication', 'date', 'type', 'information', )
    ordering = ['publication', 'date', 'type', 'information', ]


class NameTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class CreatorNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )
    ordering = ['name', 'type', ]


class NameIdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identifier_schema', 'schema_uri', )
    ordering = ['identifier', 'identifier_schema', 'schema_uri', ]


class AffiliationIdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identifier_schema', 'schema_uri', )
    ordering = ['identifier', 'identifier_schema', 'schema_uri', ]


class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', )
    ordering = ['name', 'identifier', ]


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('publication', 'name', 'given_name', 'family_name', 'name_identifier', 'affiliation', )
    ordering = ['publication', 'name', 'given_name', 'family_name', 'name_identifier', 'affiliation', ]


class TitleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name', ]


class TitleAdmin(admin.ModelAdmin):
    list_display = ('publication', 'name', 'type', )
    ordering = ['publication', 'name', 'type', ]


admin.site.register(publications.models.IdentifierType, IdentifierTypeAdmin)
admin.site.register(publications.models.Identifier, IdentifierAdmin)
admin.site.register(publications.models.ResourceTypeGeneral, ResourceTypeGeneralAdmin)
admin.site.register(publications.models.ResourceType, ResourceTypeAdmin)
admin.site.register(publications.models.Publication, PublicationAdmin)
admin.site.register(publications.models.Size, SizeAdmin)
admin.site.register(publications.models.Format, FormatAdmin)
admin.site.register(publications.models.Rights, RightsAdmin)
admin.site.register(publications.models.FunderIdentifier, FunderIdentifierAdmin)
admin.site.register(publications.models.Award, AwardAdmin)
admin.site.register(publications.models.FundingReference, FundingReferenceAdmin)
admin.site.register(publications.models.RelationType, RelationTypeAdmin)
admin.site.register(publications.models.RelatedIdentifierType, RelatedIdentifierTypeAdmin)
admin.site.register(publications.models.RelatedIdentifier, RelatedIdentifierAdmin)
admin.site.register(publications.models.DateType, DateTypeAdmin)
admin.site.register(publications.models.Date, DateAdmin)
admin.site.register(publications.models.NameType, NameTypeAdmin)
admin.site.register(publications.models.CreatorName, CreatorNameAdmin)
admin.site.register(publications.models.NameIdentifier, NameIdentifierAdmin)
admin.site.register(publications.models.AffiliationIdentifier, AffiliationIdentifierAdmin)
admin.site.register(publications.models.Affiliation, AffiliationAdmin)
admin.site.register(publications.models.Creator, CreatorAdmin)
admin.site.register(publications.models.TitleType, TitleTypeAdmin)
admin.site.register(publications.models.Title, TitleAdmin)
