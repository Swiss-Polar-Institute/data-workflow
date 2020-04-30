# Generated by Django 3.0.3 on 2020-04-30 15:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the affiliation. If a research group name has already been used for the creator, then the organisation to which thisgroup formally belongs could be used here.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='Code assigned by the funder to a sponsered award (grant).', max_length=50)),
                ('uri', models.URLField(blank=True, help_text='The URI leading to a page provided by the funder for more information about the award (grant).', null=True)),
            ],
            options={
                'unique_together': {('number', 'uri')},
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(blank=True, help_text='Personal or first name of the creator.', max_length=50, null=True)),
                ('family_name', models.CharField(blank=True, help_text='Surname or last name of the creator.', max_length=50, null=True)),
                ('affiliation', models.ManyToManyField(blank=True, help_text='Organisational or institutional affiliations of the creator.', to='publications.Affiliation')),
            ],
        ),
        migrations.CreateModel(
            name='DateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of date.', max_length=50, unique=True)),
                ('description', models.TextField(help_text='Description of type according to DataCite Metadata Schema v4.3.', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Technical format of a resource where this is listed as a Mime type (not required by DataCite).', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundingReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funder_name', models.CharField(help_text='Name of the funding provider.', max_length=200)),
                ('award_title', models.CharField(blank=True, help_text='Human readable name or title of the award (grant).', max_length=500, null=True)),
                ('award_number', models.OneToOneField(blank=True, help_text='The code assigned by the funder to a sponsored award (grant).', null=True, on_delete=django.db.models.deletion.PROTECT, to='publications.Award')),
            ],
            options={
                'unique_together': {('funder_name', 'award_number')},
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(help_text='Unique identifier that identifies a resource. This can relate to a specific version or all versions.', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of an identifier type', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NameType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of name', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the publisher.', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelatedIdentifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of related identifier', max_length=50, unique=True)),
                ('description', models.TextField(help_text='Description of type according to DataCite Metadata Schema v4.3.', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Description of relationship between resource being registered and related resource.', max_length=50, unique=True)),
                ('description', models.TextField(help_text='Description of type according to DataCite Metadata Schema v4.3.', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceTypeGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of a resource', max_length=50, unique=True)),
                ('description', models.TextField(help_text='Description of type according to DataCite Metadata Schema v4.3.', max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'Resource types general',
            },
        ),
        migrations.CreateModel(
            name='Rights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(help_text='Rights information for a resource.', max_length=1000)),
                ('uri', models.URLField(blank=True, help_text='URI of the license', null=True)),
            ],
            options={
                'verbose_name_plural': 'Rights',
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of a schema (not a DataCite model).', max_length=100, unique=True)),
                ('uri', models.CharField(help_text='URI of a schema.', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SizeUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(help_text='Units of a measurement of size (not a DataCite field).', max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TitleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of title.', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Free text description of a resource, preferably one term, description of the resource that can be combined with the sub-property.', max_length=50)),
                ('type_general', models.ForeignKey(help_text='General type of a resource.', on_delete=django.db.models.deletion.PROTECT, to='publications.ResourceTypeGeneral')),
            ],
            options={
                'unique_together': {('description', 'type_general')},
            },
        ),
        migrations.CreateModel(
            name='RelatedIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200, unique=True)),
                ('related_identifier_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications.RelatedIdentifierType')),
                ('relation_type', models.ForeignKey(help_text='Description of relationship between resource being registered and related resource.', on_delete=django.db.models.deletion.PROTECT, to='publications.RelationType')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_year', models.IntegerField(help_text='The year when the data was or will be made publicly available. In the case of resources such as software or dynamic data where there may be multiple releases in one year, include the Date/dateType/dateInformation property and sub-properties to provide more information about the publication or release date details. Format: YYYY. If an embargo period has been in effect, use the date when the embargo period ends. In the case of datasets, "publish" is understood to mean making the 15 data available on a specific date to the community of researchers. If there is no standard publication year value, use the date that would be preferred from a citation perspective. ', validators=[django.core.validators.MinValueValidator(2016), django.core.validators.MaxValueValidator(2050)])),
                ('size_bytes', models.IntegerField(help_text='Size of the resource in bytes (not a DataCite field).', validators=[django.core.validators.MinValueValidator(0)])),
                ('version', models.CharField(blank=True, help_text='Version number of the resource.', max_length=10, null=True)),
                ('creator', models.ManyToManyField(help_text='Main researchers involved in the publication, or authors of the publication, in order of priority. This can be an organisation or a person.', to='publications.Creator')),
                ('format', models.ManyToManyField(blank=True, help_text='Formats of the resource.', to='publications.Format')),
                ('funding', models.ManyToManyField(blank=True, help_text='Information about funding or financial information for the resource being registered.', to='publications.FundingReference')),
                ('identifier', models.OneToOneField(help_text='Unique identifier that identifies a resource. This can relate to a specific version or all versions.', on_delete=django.db.models.deletion.PROTECT, to='publications.Identifier')),
                ('publisher', models.ForeignKey(help_text='The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role. For software, use Publisher for the code repository. If there is an entity other than a code repository, that "holds, archives, publishes, prints, distributes, releases, issues, or produces" the code, use the property Contributor/contributorType/hostingInstitution for the code repository.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publisher')),
                ('related_identifier', models.ManyToManyField(blank=True, help_text='Publication to which the identifier relates.', to='publications.RelatedIdentifier')),
                ('resource_type', models.ForeignKey(help_text='Description of the resource.', on_delete=django.db.models.deletion.PROTECT, to='publications.ResourceType')),
                ('rights', models.ForeignKey(blank=True, help_text='Any rights information for this resource.The property may be repeated to record complex rights characteristics.', null=True, on_delete=django.db.models.deletion.PROTECT, to='publications.Rights')),
            ],
        ),
        migrations.AddField(
            model_name='identifier',
            name='type',
            field=models.ForeignKey(help_text='Type of identifier', on_delete=django.db.models.deletion.PROTECT, to='publications.IdentifierType'),
        ),
        migrations.CreateModel(
            name='CreatorName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full name of the creator. For a personal name, the format should be family name,given name. Non-roman names may be transliterated according to ALA-LC schemas.', max_length=100)),
                ('type', models.ForeignKey(blank=True, help_text='The type of name.', null=True, on_delete=django.db.models.deletion.PROTECT, to='publications.NameType')),
            ],
            options={
                'unique_together': {('name', 'type')},
            },
        ),
        migrations.AddField(
            model_name='creator',
            name='name',
            field=models.OneToOneField(help_text='Creator of the publication.', on_delete=django.db.models.deletion.PROTECT, to='publications.CreatorName'),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name or title of a resource.', max_length=500)),
                ('publication', models.ForeignKey(help_text='Publication named by the title.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publication')),
                ('type', models.ForeignKey(help_text='Type of title.', on_delete=django.db.models.deletion.PROTECT, to='publications.TitleType')),
            ],
            options={
                'unique_together': {('publication', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(help_text='Size of resource. Free text to include data volume, pages, time etc.', max_length=50)),
                ('publication', models.ForeignKey(help_text='Publication described by the size.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publication')),
                ('units', models.ForeignKey(help_text='Units of measurement (not a DataCite field). Note that there is a separate field for size of the resource in bytes.', on_delete=django.db.models.deletion.PROTECT, to='publications.SizeUnits')),
            ],
            options={
                'unique_together': {('publication', 'size', 'units')},
            },
        ),
        migrations.CreateModel(
            name='RightsIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('identifier_schema', models.ForeignKey(help_text='Schema to which the identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Schema')),
                ('rights', models.ForeignKey(help_text='Rights identified by the unique identifier.', on_delete=django.db.models.deletion.PROTECT, to='publications.Rights')),
            ],
            options={
                'abstract': False,
                'unique_together': {('identifier', 'identifier_schema')},
            },
        ),
        migrations.CreateModel(
            name='PublisherIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('identifier_schema', models.ForeignKey(help_text='Schema to which the identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Schema')),
                ('publisher', models.ForeignKey(help_text='Publisher identified by the unique identifier.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publisher')),
            ],
            options={
                'abstract': False,
                'unique_together': {('identifier', 'identifier_schema')},
            },
        ),
        migrations.CreateModel(
            name='NameIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('creator', models.ForeignKey(help_text='Creator to which the unique name identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Creator')),
                ('identifier_schema', models.ForeignKey(help_text='Schema to which the identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Schema')),
            ],
            options={
                'unique_together': {('creator', 'identifier')},
            },
        ),
        migrations.CreateModel(
            name='FunderIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('funding_reference', models.ForeignKey(help_text='Funder identified by the unique identifier.', on_delete=django.db.models.deletion.PROTECT, to='publications.FundingReference')),
                ('identifier_schema', models.ForeignKey(help_text='Schema to which the identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Schema')),
            ],
            options={
                'abstract': False,
                'unique_together': {('identifier', 'identifier_schema')},
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Date relevant to the work.')),
                ('information', models.CharField(blank=True, help_text='Free text information about a date.', max_length=500, null=True)),
                ('publication', models.ForeignKey(help_text='Publication to which the date is relevant.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publication')),
                ('type', models.ForeignKey(help_text='Type of date', on_delete=django.db.models.deletion.PROTECT, to='publications.DateType')),
            ],
            options={
                'unique_together': {('publication', 'date', 'type')},
            },
        ),
        migrations.CreateModel(
            name='AffiliationIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('affiliation', models.ForeignKey(help_text='Affiliation identified by the unique identifier.', on_delete=django.db.models.deletion.PROTECT, to='publications.Affiliation')),
                ('identifier_schema', models.ForeignKey(help_text='Schema to which the identifier belongs.', on_delete=django.db.models.deletion.PROTECT, to='publications.Schema')),
            ],
            options={
                'abstract': False,
                'unique_together': {('identifier', 'identifier_schema')},
            },
        ),
    ]
