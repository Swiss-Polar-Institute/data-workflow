from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator


# Models below for the publications are based on the DataCite Metadata Schema version 4.3:
# DataCite Metadata Working Group. (2019). DataCite Metadata Schema Documentation for the Publication and Citation
# of Research Data. Version 4.3. DataCite e.V. https://doi.org/10.14454/7xq3-zf69


class IdentifierType(models.Model):
    """
    Type of identifier as from list in DataCite Metadata Schema version 4.3
    """

    name = models.CharField(help_text='Name of an identifier type', max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Identifier(models.Model):
    """
    Unique identifier of a publication or resource.
    """
    uri = models.CharField(help_text='Unique identifier that identifies a resource. This can relate to a '
                                     'specific version or all versions.', max_length=255, unique=True, blank=False,
                           null=False)
    type = models.ForeignKey(IdentifierType, help_text='Type of identifier', blank=False,
                             null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.type, self.uri)


class ResourceTypeGeneral(models.Model):
    """
    General type of a resource.
    """
    name = models.CharField(max_length=50, help_text='Type of a resource', blank=False, null=False, unique=True)
    description = models.TextField(max_length=1000,
                                   help_text='Description of type according to DataCite Metadata Schema v4.3.',
                                   blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = 'Resource types general'


class ResourceType(models.Model):
    """
    Description of a resource.
    """
    description = models.CharField(max_length=50, help_text='Free text description of a resource, preferably one term,'
                                                            ' description of the resource that can be combined with '
                                                            'the sub-property.', blank=False, null=False)
    type_general = models.OneToOneField(ResourceTypeGeneral, help_text='General type of a resource.', blank=False,
                                        null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.type_general)

    class Meta:
        unique_together = (('description', 'type_general'),)


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
        unique_together = (('identifier', 'identifier_schema'),)


class AffiliationIdentifier(AbstractIdentifier):
    """
    Uniquely identifies the organisational affiliation of the creator
    """

    def __str__(self):
        return "{} {}".format(self.identifier_schema, self.identifier)


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

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = (('name', 'identifier'),)


class NameType(models.Model):
    """
    Type of name.
    """
    name = models.CharField(max_length=50, help_text='Type of name', blank=False, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class CreatorName(models.Model):
    """
    Full name of the creator.
    """
    name = models.CharField(max_length=100,
                            help_text='Full name of the creator. For a personal name, the format should be family name,'
                                      'given name. Non-roman names may be transliterated according to ALA-LC schemas.',
                            blank=False, null=False)
    type = models.ForeignKey(NameType, help_text='The type of name.', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = (('name', 'type'),)


class Creator(models.Model):
    """
    Main researchers involved in the publication, or authors of the publication, in order of priority. This can be an
    organisation or a person.
    """
    name = models.OneToOneField(CreatorName, help_text='Creator of the publication.', blank=False, null=False,
                                on_delete=models.PROTECT)
    given_name = models.CharField(max_length=50, help_text='Personal or first name of the creator.', blank=True,
                                  null=True)
    family_name = models.CharField(max_length=50, help_text='Surname or last name of the creator.', blank=True,
                                   null=True)
    affiliation = models.ManyToManyField(Affiliation,
                                    help_text='Organisational or institutional affiliations of the creator.', blank=True)

    # def __str__(self):
    #     publications = self.publication.all()
    #     publication_identifiers = []
    #
    #     for publication in publications:
    #         publication_identifiers.append(publication.identifier.uri)
    #
    #     publication_str = ";".join(publication_identifiers)
    #
    #     return "{} {}. {}. Publications:{}".format(self.given_name, self.family_name, self.affiliation, publication_str)
    #
    # def main_name_identifiers(self):
    #     main_name_identifiers = NameIdentifier.objects.filter(creator=self)
    #
    #     return main_name_identifiers
    #
    # def main_affiliations(self):
    #     main_affiliations = Affiliation.objects.filter(creator=self)
    #
    #     return main_affiliations


class NameIdentifier(AbstractIdentifier):
    """
    Uniquely identifies an individual or organisation according to various schemas.
    """
    creator = models.ForeignKey(Creator, help_text='Creator to which the unique name identifier belongs.', blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.identifier_schema, self.identifier)


class Publication(models.Model):
    """
    Describes a publication according to the DataCite Metadata Schema version 4.3.
    """

    identifier = models.OneToOneField(Identifier,
                                      help_text='Unique identifier that identifies a resource. This can relate to a '
                                                'specific version or all versions.', blank=False, null=False,
                                      on_delete=models.PROTECT, unique=True)
    creator = models.ManyToManyField(Creator,
                                     help_text='Main researchers involved in the publication, or authors of the '
                                               'publication, in order of priority. This can be an organisation or a '
                                               'person.', blank=False)
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
    version = models.CharField(max_length=10, help_text='Version number of the resource.', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not hasattr(self, 'title'):
            raise ValidationError('Publication needs to have a title')

        with transaction.atomic():
            super().save(*args, **kwargs)

            Title.objects.update_or_create(
                publication=self, type=getattr(self, 'title_type'), defaults={'name': getattr(self, 'title')}
            )

    def main_title(self):

        try:
            main_title = Title.objects.get(publication=self, type__name='MainTitle')
        except ObjectDoesNotExist:
            return "Unknown title"

        return main_title.name

    # def main_creators(self):
    #
    #     main_creators = Creator.objects.filter(publication=self)
    #
    #     return main_creators

    def __str__(self):
        return "{} ({}). Version: {}. {}. {}.".format(self.main_title(), self.publication_year, self.version,
                                                      self.publisher, self.identifier)


class Size(models.Model):
    """
    Size of resource. Free text to include data volume, pages, time etc.
    """
    publication = models.ForeignKey(Publication,
                                    help_text='Publication described by the size.', blank=False, null=False,
                                    on_delete=models.PROTECT)
    size = models.CharField(max_length=50,
                            help_text='Size of resource. Free text to include data volume, pages, time etc.',
                            blank=True, null=True)

    def __str__(self):
        return "{}".format(self.size)

    class Meta:
        unique_together = (('publication', 'size'),)


class Format(models.Model):
    """
    Technical format of a resource.
    """
    publication = models.ForeignKey(Publication, help_text='Publication described by a format.', blank=False,
                                    null=False,
                                    on_delete=models.PROTECT)
    format = models.CharField(max_length=100, help_text='Technical format of a resource.', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.format)

    class Meta:
        unique_together = (('publication', 'format'),)


class Rights(models.Model):
    """
    Any rights information for a resource. Property may be repeated for complex situations.
    """
    publication = models.ForeignKey(Publication, help_text='Publication to which the rights relate.', blank=False,
                                    null=False, on_delete=models.PROTECT)
    statement = models.TextField(max_length=1000, help_text='Rights information for a resource.', blank=False,
                                 null=False)
    uri = models.URLField(help_text='URI of the license', blank=True, null=True)
    identifier = models.CharField(max_length=20, help_text='Short, standardised version of the license name.',
                                  blank=False,
                                  null=False)
    identifier_scheme = models.CharField(max_length=50, help_text='Name of the scheme', blank=True, null=True)
    scheme_uri = models.URLField(help_text='URI of rights identifier scheme', blank=True, null=True)

    def __str__(self):
        return "{}. The full text of {} can be found at {}.".format(self.statement, self.identifier, self.uri)

    class Meta:
        verbose_name_plural = 'Rights'
        unique_together = (('publication', 'identifier'),)


class FunderIdentifier(models.Model):
    """
    Unique identifier of a funding entity, according to various types.
    """
    identifier = models.CharField(max_length=200,
                                  help_text='Unique identifier of a funding entity, according to various types.',
                                  unique=True)
    type = models.CharField(max_length=50, help_text='Type of the funder identifier.', blank=True, null=True)
    scheme_uri = models.URLField(help_text='URI of the funder identifier scheme.', blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.identifier, self.type)


class Award(models.Model):
    """
    The code assigned by the funder to a sponsored award (grant).
    """
    number = models.CharField(max_length=50, help_text='Code assigned by the funder to a sponsered award (grant).',
                              blank=False, null=False)
    uri = models.URLField(help_text='The URI leading to a page provided by the funder for more information about the '
                                    'award (grant).', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.number)

    class Meta:
        unique_together = (('number', 'uri'),)


class FundingReference(models.Model):
    """
    Information about funding or financial information for the resource being registered.
    """
    publication = models.ForeignKey(Publication, help_text='Publication to which the funding relates.', blank=False,
                                    null=False, on_delete=models.PROTECT)
    funder_name = models.CharField(max_length=200, help_text='Name of the funding provider.', blank=False, null=False)
    funder_identifier = models.OneToOneField(FunderIdentifier,
                                             help_text='Unique identifier of a funding entity, according to various '
                                                       'types.',
                                             blank=True, null=True, on_delete=models.PROTECT)
    award_number = models.OneToOneField(Award,
                                        help_text='The code assigned by the funder to a sponsored award (grant).',
                                        blank=True, null=True, on_delete=models.PROTECT)
    award_title = models.CharField(max_length=500, help_text='Human readable name or title of the award (grant).',
                                   blank=True, null=True)

    def __str__(self):
        return "{}. {} ({})".format(self.funder_name, self.award_title, self.award_number)

    class Meta:
        unique_together = (('publication', 'funder_name', 'award_number'),)


class RelationType(models.Model):
    """
    Description of relationship between resource being registered and related resource.
    """
    name = models.CharField(max_length=50,
                            help_text='Description of relationship between resource being registered and related '
                                      'resource.',
                            blank=False, null=False, unique=True)
    description = models.TextField(max_length=1000,
                                   help_text='Description of type according to DataCite Metadata Schema v4.3.',
                                   blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class RelatedIdentifierType(models.Model):
    """
    Type of related identifier
    """
    name = models.CharField(max_length=50, help_text='Type of related identifier', blank=False, null=False, unique=True)
    description = models.TextField(max_length=1000,
                                   help_text='Description of type according to DataCite Metadata Schema v4.3.',
                                   blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class RelatedIdentifier(models.Model):
    """
    Globally unique identifiers of related resources.
    """
    publication = models.ForeignKey(Publication, help_text='Publication to which the identifier relates.', blank=False,
                                    null=False, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=200,
                                  help_text='Uniquely identifies an item according to various schemas.', blank=False,
                                  null=False)
    related_identifier_type = models.ForeignKey(RelatedIdentifierType, blank=False, null=False,
                                                on_delete=models.PROTECT)
    relation_type = models.ForeignKey(RelationType,
                                      help_text='Description of relationship between resource being registered and '
                                                'related resource.',
                                      blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {} ({})".format(self.relation_type, self.identifier, self.related_identifier_type)

    class Meta:
        unique_together = (('publication', 'identifier'),)


class DateType(models.Model):
    """
    Type of date.
    """
    name = models.CharField(max_length=50, help_text='Type of date.', blank=False, null=False, unique=True)
    description = models.TextField(max_length=1000,
                                   help_text='Description of type according to DataCite Metadata Schema v4.3.',
                                   blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class Date(models.Model):
    """
    Dates relevant to the work.
    """
    publication = models.ForeignKey(Publication, help_text='Publication to which the date is relevant.', blank=False,
                                    null=False, on_delete=models.PROTECT)
    date = models.DateField(help_text='Date relevant to the work.', blank=False, null=False)
    type = models.ForeignKey(DateType, help_text='Type of date', blank=False, null=False, on_delete=models.PROTECT)
    information = models.CharField(max_length=500, help_text='Free text information about a date.', blank=True,
                                   null=True)

    def __str__(self):
        return "{}: {}".format(self.type, self.date)

    class Meta:
        unique_together = (('publication', 'date', 'type'),)

















class TitleType(models.Model):
    """
    Type of title of resource.
    """
    name = models.CharField(max_length=50, help_text='Type of title.', blank=False, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Title(models.Model):
    """
    Name or title of a resource.
    """
    publication = models.ForeignKey(Publication, help_text='Publication named by the title.', blank=False, null=False,
                                    on_delete=models.PROTECT)
    name = models.CharField(max_length=500, help_text='Name or title of a resource.', blank=False, null=False)
    type = models.ForeignKey(TitleType, help_text='Type of title.', blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = (('publication', 'type'),)
