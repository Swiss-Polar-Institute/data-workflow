from django.db import models


# Models below for the publications are based on the DataCite Metadata Schema version 4.3:
# DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation
# of Research Data. Version 4.3. DataCite e.V. https://doi.org/10.14454/7xq3-zf69

class IdentifierType(models.Model):
    """
    Type of identifier as from list in DataCite Metadata Schema version 4.3
    """

    name = models.CharField(help_text='Name of an identifier type', max_length=50, blank=False, null=False)


class Identifier(models.Model):
    """
    Unique identifier of a publication or resource.
    """
    uri = models.CharField(help_text='Unique identifier that identifies a resource. This can relate to a '
                                     'specific version or all versions.', max_length=255, unique=True, blank=False,
                           null=True)
    type = models.ForeignKey(IdentifierType, help_text='Type of identifier', on_delete=models.PROTECT)


class NameType(models.Model):
    """
    Type of name.
    """
    name = models.CharField(max_length=50, help_text='Type of name', blank=False, null=False)


class CreatorName(models.Model):
    """
    Full name of the creator.
    """
    name = models.CharField(max_length=100,
                            help_text='Full name of the creator. For a personal name, the format should be family name,'
                                      'given name. Non-roman names may be transliterated according to ALA-LC schemas.',
                            blank=False, null=False)
    type = models.ForeignKey(NameType, help_text='The type of name.', blank=False, null=False)


class AbstractIdentifier(models.model):
    """
    Uniquely identifies an item according to various schemas.
    """
    identifier = models.CharField(max_length=200,
                                  help_text='Uniquely identifies an item according to various schemas.')
    identifier_schema = models.CharField(max_length=200, help_text='Name of the identifier schema.',
                                              blank=False, null=False)
    schema_uri = models.URLField(max_length=100, help_text='URI of the identifier schema.', blank=True, null=True)

    class Meta:
        abstract = True


class NameIdentifier(AbstractIdentifier):
    """
    Uniquely identifies an individual or organisation according to various schemas.
    """


class AffiliationIdentifier(AbstractIdentifier):
    """
    Uniquely identifies the organisational affiliation of the creator
    """


class Affiliation(models.Model):
    """
    Organisational or institutional affiliation of the creator.
    """
    name = models.CharField(max_length=200, help_text='Name of the affiliation. If a research group name has already '
                                                      'been used for the creator, then the organisation to which this'
                                                      'group formally belongs could be used here.', blank=False,
                            null=False)
    identifier = models.OneToOneField(AffiliationIdentifier, max_length=200,
                                      help_text='Uniquely identifies the organisational affiliation of the creator.',
                                      blank=True, null=True)


class Creator(models.Model):
    """
    Main researchers involved in the publication, or authors of the publication, in order of priority. This can be an
    organisation or a person.
    """
    name = models.OneToOneField(CreatorName, help_text='Creator of the publication.', on_delete=models.PROTECT)
    given_name = models.CharField(max_length=50, help_text='Personal or first name of the creator.', blank=True,
                                  null=True)
    family_name = models.CharField(max_length=50, help_text='Surname or last name of the creator.', blank=True,
                                   null=True)
    name_identifier = models.ForeignKey(NameIdentifier,
                                        help_text='Uniquely identifies an individual or organisation according to various schemas.',
                                        on_delete=models.PROTECT)
    affiliation = models.ForeignKey(Affiliation,
                                    help_text='Organisational or institutional affiliation of the creator.',
                                    on_delete=models.PROTECT, blank=True, null=True)


class Publication(models.Model):
    """
    Describes a publication according to the DataCite Metadata Schema version 4.3.
    """

    identifier = models.OneToOneField(Identifier,
                                      help_text='Unique identifier that identifies a resource. This can relate to a '
                                                'specific version or all versions.', on_delete=models.PROTECT)
    creator = models.ForeignKey(Creator,
                                help_text='Main researchers involved in the publication, or authors of the publication,'
                                          'in order of priority. This can be an organisation or a person.',
                                on_delete=models.PROTECT)
