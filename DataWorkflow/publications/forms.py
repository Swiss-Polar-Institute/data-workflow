from django import forms

import publications
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


class CreatorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.id:
            name = self.instance.name()
        else:
            name = None
        self.fields['name'] = forms.CharField(label='Name', max_length=100, initial=name)

    # def save(self, *args, **kwargs):
    #     title = self.cleaned_data['title']
    #
    #     creator = super().save(*args, **kwargs)
    #     creator.name = name
    #     creator.name_type = CreatorName.objects.get(name='MainTitle')
    #
    #     creator.save()
    #
    #     return creator


#
# class PublicationExtendedForm(PublicationForm):
#
#     def __init__(self, *args, **kwargs):
#         super(PublicationExtendedForm, self).__init__(*args, **kwargs)
#         self.fields['title'] = forms.CharField(label='Title', max_length=75)
