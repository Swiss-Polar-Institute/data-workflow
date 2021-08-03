from django.contrib import admin
import publications.models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _


# Register your models here.
from publications.forms import PublicationForm

class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'username', 'password1', 'password2',)
    }),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'uri',)
    ordering = ['name', 'uri', ]


class IdentifierTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('uri', 'type',)
    ordering = ['uri', 'type', ]


class ResourceTypeGeneralAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ['name', 'description', ]


class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'type_general',)
    ordering = ['description', 'type_general', ]


class PublisherIdentifierAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'identifier', 'identifier_schema',)
    ordering = ['publisher', 'identifier', 'identifier_schema', ]


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        'main_title', 'identifier', 'creator_list', 'title_list', 'publisher', 'publication_year', 'resource_type',
        'related_identifier_list', 'size_bytes', 'format_list', 'version', 'rights', 'funding_list',)
    ordering = ['identifier', 'publisher', 'publication_year', 'resource_type', 'size_bytes', 'version', 'rights', ]

    def creator_list(self, obj):
        creators = obj.creator.all()

        return ", ".join([creator.name for creator in creators])

    def title_list(self, obj):
        titles = obj.title.all()

        return ", ".join([title.name for title in titles])

    def format_list(self, obj):
        formats = obj.format.all()

        return ", ".join([format.name for format in formats])

    def funding_list(self, obj):
        funding_references = obj.funding.all()

        return ", ".join([funding_reference.funder_name for funding_reference in funding_references])

    def related_identifier_list(self, obj):
        related_identifiers = obj.related_identifier.all()

        return ", ".join([related_identifier.identifier for related_identifier in related_identifiers])

    class Meta:
        form = PublicationForm
        fields = ('identifier', 'publisher', 'publication_year', 'resource_type', 'version', 'size_bytes', 'main_title')


class SizeUnitsAdmin(admin.ModelAdmin):
    list_display = ('unit',)
    ordering = ['unit', ]


class SizeAdmin(admin.ModelAdmin):
    list_display = ('publication', 'size', 'units',)
    ordering = ['publication', 'size', 'units', ]


class FormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class RightsAdmin(admin.ModelAdmin):
    list_display = ('statement', 'uri',)
    ordering = ['statement', 'uri', ]


class RightsIdentifierAdmin(admin.ModelAdmin):
    list_display = ('rights', 'identifier', 'identifier_schema',)
    ordering = ['rights', 'identifier', 'identifier_schema', ]


class FunderIdentifierAdmin(admin.ModelAdmin):
    list_display = ('funding_reference', 'identifier', 'identifier_schema',)
    ordering = ['funding_reference', 'identifier', 'identifier_schema', ]


class AwardAdmin(admin.ModelAdmin):
    list_display = ('number', 'uri',)
    ordering = ['number', 'uri', ]


class FundingReferenceAdmin(admin.ModelAdmin):
    list_display = ('funder_name', 'award_number', 'award_title',)
    ordering = ['funder_name', 'award_number', 'award_title', ]


class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ['name', 'description', ]


class RelatedIdentifierTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ['name', 'description', ]


class RelatedIdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'related_identifier_type', 'relation_type',)
    ordering = ['identifier', 'related_identifier_type', 'relation_type', ]


class DateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ['name', 'description', ]


class DateAdmin(admin.ModelAdmin):
    list_display = ('publication', 'date', 'type', 'information',)
    ordering = ['publication', 'date', 'type', 'information', ]


class NameTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class CreatorNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    ordering = ['name', 'type', ]


class NameIdentifierAdmin(admin.ModelAdmin):
    list_display = ('creator', 'identifier', 'identifier_schema',)
    ordering = ['creator', 'identifier', 'identifier_schema', ]


class AffiliationIdentifierAdmin(admin.ModelAdmin):
    list_display = ('affiliation', 'identifier', 'identifier_schema',)
    ordering = ['affiliation', 'identifier', 'identifier_schema', ]


class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'given_name', 'family_name', 'affiliation_list',)
    ordering = ['name', 'given_name', 'family_name', ]

    def affiliation_list(self, obj):
        affiliations = obj.affiliation.all()

        return ", ".join([affiliation.name for affiliation in affiliations])


class TitleTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name', ]


class TitleAdmin(admin.ModelAdmin):
    list_display = ('publication', 'name', 'type',)
    ordering = ['publication', 'name', 'type', ]


admin.site.register(publications.models.Schema, SchemaAdmin)
admin.site.register(publications.models.IdentifierType, IdentifierTypeAdmin)
admin.site.register(publications.models.Identifier, IdentifierAdmin)
admin.site.register(publications.models.ResourceTypeGeneral, ResourceTypeGeneralAdmin)
admin.site.register(publications.models.ResourceType, ResourceTypeAdmin)
admin.site.register(publications.models.Publisher, PublisherAdmin)
admin.site.register(publications.models.PublisherIdentifier, PublisherIdentifierAdmin)
admin.site.register(publications.models.Publication, PublicationAdmin)
admin.site.register(publications.models.SizeUnits, SizeUnitsAdmin)
admin.site.register(publications.models.Size, SizeAdmin)
admin.site.register(publications.models.Format, FormatAdmin)
admin.site.register(publications.models.Rights, RightsAdmin)
admin.site.register(publications.models.RightsIdentifier, RightsIdentifierAdmin)
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
