# Generated by Django 3.0.3 on 2020-04-23 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0008_plural_resource_type_general'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='title',
            unique_together={('publication', 'type')},
        ),
    ]