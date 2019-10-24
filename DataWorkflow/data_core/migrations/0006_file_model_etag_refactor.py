# Generated by Django 2.2.6 on 2019-10-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0005_adds_sha1_in_abstract_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='md5',
        ),
        migrations.AddField(
            model_name='file',
            name='etag',
            field=models.CharField(default=None, help_text='ETag of the file', max_length=35),
            preserve_default=False,
        ),
    ]
