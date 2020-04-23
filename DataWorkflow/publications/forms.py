from django import forms

from .models import Publication


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ('main_title', 'identifier', 'publisher', 'publication_year', 'resource_type', 'version')