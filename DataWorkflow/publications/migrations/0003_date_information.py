# Generated by Django 3.0.3 on 2020-04-23 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_final_publications_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datetype',
            name='information',
        ),
        migrations.AddField(
            model_name='date',
            name='information',
            field=models.CharField(blank=True, help_text='Free text information about a date.', max_length=500, null=True),
        ),
    ]