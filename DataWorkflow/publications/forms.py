from django import forms

from .models import Publication


class PublicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'] = forms.CharField(label='Title', max_length=200)

    def save(self, *args, **kwargs):
        title = self.cleaned_data['title']

        publication = super().save(commit=False)
        publication.title = title
        publication.type = None

        publication.save()

    class Meta:
        model = Publication
        fields = ('identifier', 'publisher', 'publication_year', 'resource_type', 'version')