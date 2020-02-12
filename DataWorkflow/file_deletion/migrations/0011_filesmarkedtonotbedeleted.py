# Generated by Django 2.2.6 on 2020-01-16 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0015_dbindex_osk_maxlength'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_deletion', '0010_remove_batch_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesMarkedToNotBeDeleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('reason', models.CharField(choices=[('RD', 'Required Duplicate')], help_text='Reason for which the file is marked not to be deleted', max_length=2)),
                ('batch', models.ForeignKey(help_text='Batch of the file added', on_delete=django.db.models.deletion.PROTECT, to='file_deletion.Batch')),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='file_deletion_filesmarkedtonotbedeleted_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('file', models.ForeignKey(help_text='File that has been added to this table', on_delete=django.db.models.deletion.PROTECT, to='data_core.File')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='file_deletion_filesmarkedtonotbedeleted_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Files to not be deleted',
            },
        ),
    ]