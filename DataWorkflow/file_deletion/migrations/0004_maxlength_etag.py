# Generated by Django 2.2.6 on 2019-10-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_deletion', '0003_etag_maxlength'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedfile',
            name='etag',
            field=models.CharField(db_index=True, help_text='ETag of the file', max_length=50),
        ),
    ]