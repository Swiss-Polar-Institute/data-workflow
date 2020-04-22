from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
                           null=False)
    type = models.ForeignKey(IdentifierType, help_text='Type of identifier', blank=False,
                             null=False, on_delete=models.PROTECT)


class ResourceTypeGeneral(models.Model):
    """
    General type of a resource.
    """
    name = models.CharField(max_length=50, help_text='Type of a resource', blank=False, null=False)


class ResourceType(models.Model):
    """
    Description of a resource.
    """
    description = models.CharField(max_length=50, help_text='Free text description of a resource, preferably one term,'
                                                            ' description of the resource that can be combined with '
                                                            'the sub-property.', blank=False, null=False)
    type_general = models.OneToOneField(ResourceTypeGeneral, help_text='General type of a resource.', blank=False,
                                        null=False)


class Publication(models.Model):
    """
    Describes a publication according to the DataCite Metadata Schema version 4.3.
    """

    identifier = models.OneToOneField(Identifier,
                                      help_text='Unique identifier that identifies a resource. This can relate to a '
                                                'specific version or all versions.', blank=False, null=False,
                                      on_delete=models.PROTECT)
    publisher = models.CharField(max_length=500, help_text='The name of the entity that holds, archives, publishes '
                                                           'prints, distributes, releases, issues, or produces the '
                                                           'resource. This property will be used to formulate the '
                                                           'citation, so consider the prominence of the role. For '
                                                           'software, use Publisher for the code repository. If there '
                                                           'is an entity other than a code repository, that "holds, '
                                                           'archives, publishes, prints, distributes, releases, issues,'
                                                           ' or produces" the code, use the property '
                                                           'Contributor/contributorType/hostingInstitution for the code'
                                                           ' repository.', blank=False, null=False)
    publication_year = models.IntegerField(help_text='The year when the data was or will be made publicly available. '
                                                     'In the case of resources such as software or dynamic data where '
                                                     'there may be multiple releases in one year, include the '
                                                     'Date/dateType/dateInformation property and sub-properties to '
                                                     'provide more information about the publication or release date '
                                                     'details. Format: YYYY. If an embargo period has been in effect, '
                                                     'use the date when the embargo period ends. In the case of '
                                                     'datasets, "publish" is understood to mean making the 15 data '
                                                     'available on a specific date to the community of researchers. If '
                                                     'there is no standard publication year value, use the date that '
                                                     'would be preferred from a citation perspective. ',
                                           validators=[MinValueValidator(2016), MaxValueValidator(2050)], blank=False,
                                           null=False)
    resource_type = models.OneToOneField(ResourceType, help_text='Description of the resource.', blank=False,
                                         null=False, on_delete=models.PROTECT)


class DateType(models.Model):
    """
    Type of date.
    """
    name = models.CharField(max_length=50, help_text='Type of date.', blank=False, null=False)


class Date(models.Model):
    """
    Dates relevant to the work.
    """
    publication = models.ForeignKey(Publication, help_text='Publication to which the date is relevant.', blank=False,
                                    null=False, on_delete=models.PROTECT)
    date = models.DateField(help_text='Date relevant to the work.', blank=False, null=False)
    type = models.ForeignKey(DateType, help_text='Type of date', blank=False, null=False)


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
    type = models.ForeignKey(NameType, help_text='The type of name.', blank=True, null=True, on_delete=models.PROTECT)


class AbstractIdentifier(models.Model):
    """
    Uniquely identifies an item according to various schemas.
    """
    identifier = models.CharField(max_length=200,
                                  help_text='Uniquely identifies an item according to various schemas.', blank=False,
                                  null=False)
    identifier_schema = models.CharField(max_length=200, help_text='Name of the identifier schema.',
                                         blank=False, null=False)
    schema_uri = models.URLField(max_length=100, help_text='URI of the identifier schema.', blank=False,
                                 null=False)  # conditions here are required for the AffiliationIdentifier. They could

    # be relaxed for the NameIdentifier.

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
                                      blank=True, null=True, on_delete=models.PROTECT)


class Creator(models.Model):
    """
    Main researchers involved in the publication, or authors of the publication, in order of priority. This can be an
    organisation or a person.
    """
    publication = models.ForeignKey(Publication,
                                    help_text='Publication in which this creator has been involved or authored.',
                                    blank=False, null=False, on_delete=models.PROTECT)
    name = models.OneToOneField(CreatorName, help_text='Creator of the publication.', blank=False, null=False,
                                on_delete=models.PROTECT)
    given_name = models.CharField(max_length=50, help_text='Personal or first name of the creator.', blank=True,
                                  null=True)
    family_name = models.CharField(max_length=50, help_text='Surname or last name of the creator.', blank=True,
                                   null=True)
    name_identifier = models.ForeignKey(NameIdentifier,
                                        help_text='Uniquely identifies an individual or organisation according to '
                                                  'various schemas.',
                                        blank=True, null=True, on_delete=models.PROTECT)
    affiliation = models.ForeignKey(Affiliation,
                                    help_text='Organisational or institutional affiliation of the creator.', blank=True,
                                    null=True, on_delete=models.PROTECT)


class TitleType(models.Model):
    """
    Type of title of resource.
    """
    name = models.CharField(max_length=50, help_text='Type of title.', blank=False, null=False)


class Title(models.Model):
    """
    Name or title of a resource.
    """
    publication = models.ForeignKey(Publication, help_text='Publication named by the title.', blank=False, null=False,
                                    on_delete=models.PROTECT)
    name = models.CharField(max_length=500, help_text='Name or title of a resource.', blank=False, null=False)
    type = models.ForeignKey(TitleType, help_text='Type of title.', blank=True, null=True, on_delete=models.PROTECT)