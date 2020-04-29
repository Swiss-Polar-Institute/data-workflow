# Generated by Django 3.0.3 on 2020-04-29 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0009_title_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='type',
            field=models.ForeignKey(help_text='Type of title.', on_delete=django.db.models.deletion.PROTECT, to='publications.TitleType'),
        ),
    ]
