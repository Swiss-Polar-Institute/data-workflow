# Generated by Django 3.0.3 on 2020-04-30 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0007_format'),
    ]

    operations = [
        migrations.RenameField(
            model_name='format',
            old_name='format',
            new_name='name',
        ),
    ]