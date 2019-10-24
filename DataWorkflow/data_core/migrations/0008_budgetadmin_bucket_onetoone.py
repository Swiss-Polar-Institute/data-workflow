# Generated by Django 2.2.6 on 2019-10-24 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0007_bucketadministration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bucketadministration',
            options={'verbose_name_plural': 'Bucket administration'},
        ),
        migrations.AlterField(
            model_name='bucketadministration',
            name='bucket',
            field=models.OneToOneField(help_text='Bucket to which these properties relate', on_delete=django.db.models.deletion.PROTECT, to='data_core.Bucket'),
        ),
    ]
