# Generated by Django 3.0.3 on 2020-04-30 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublisherIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text='Uniquely identifies an item according to various schemas.', max_length=200)),
                ('identifier_schema', models.CharField(help_text='Name of the identifier schema.', max_length=200)),
                ('schema_uri', models.URLField(help_text='URI of the identifier schema.', max_length=100)),
            ],
            options={
                'abstract': False,
                'unique_together': {('identifier', 'identifier_schema')},
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the publisher.', max_length=200)),
                ('identifier', models.OneToOneField(blank=True, help_text='Uniquely identifies the publisher.', null=True, on_delete=django.db.models.deletion.PROTECT, to='publications.PublisherIdentifier')),
            ],
            options={
                'unique_together': {('name', 'identifier')},
            },
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.ForeignKey(help_text='The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role. For software, use Publisher for the code repository. If there is an entity other than a code repository, that "holds, archives, publishes, prints, distributes, releases, issues, or produces" the code, use the property Contributor/contributorType/hostingInstitution for the code repository.', on_delete=django.db.models.deletion.PROTECT, to='publications.Publisher'),
        ),
    ]