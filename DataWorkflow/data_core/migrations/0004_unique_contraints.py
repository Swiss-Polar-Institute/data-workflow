# Generated by Django 2.2.6 on 2019-10-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0003_remove_bucket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='friendly_name',
            field=models.CharField(help_text='Friendly name of bucket', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='name',
            field=models.CharField(help_text='Bucket UUID name', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='name',
            field=models.CharField(help_text='Name of endpoint or service provider', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='sourcefile',
            name='name',
            field=models.CharField(help_text='Name of file', max_length=150, unique=True),
        ),
    ]
