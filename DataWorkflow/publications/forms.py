from django import forms

from .models import Publication, TitleType


class PublicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.id:
            main_title = self.instance.main_title()
        else:
            main_title = None
        self.fields['title'] = forms.CharField(label='Title', max_length=500, initial=main_title)

    def save(self, *args, **kwargs):
        title = self.cleaned_data['title']

        publication = super().save(*args, **kwargs)
        publication.title = title
        publication.title_type = TitleType.objects.get(name='MainTitle')

        publication.save()

        return publication

    class Meta:
        model = Publication
        fields = ('identifier', 'publisher', 'publication_year', 'resource_type', 'version')
