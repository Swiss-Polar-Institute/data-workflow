# Generated by Django 2.2.6 on 2019-10-24 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0009_etag_maxlength'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='filename',
            field=models.CharField(default=None, help_text='Filename', max_length=128),
            preserve_default=False,
        ),
    ]