# Generated by Django 2.2.6 on 2019-10-30 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_deletion', '0008_rename_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='filetobedeleted',
            name='batch',
            field=models.ForeignKey(default='', help_text='Batch of the file added', on_delete=django.db.models.deletion.PROTECT, to='file_deletion.Batch'),
            preserve_default=False,
        ),
    ]