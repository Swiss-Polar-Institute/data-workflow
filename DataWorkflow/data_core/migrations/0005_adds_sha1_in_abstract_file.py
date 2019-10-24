# Generated by Django 2.2.6 on 2019-10-24 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_core', '0004_unique_contraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='sha1_unique_together',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together={('sha1_unique_together',)},
        ),
    ]
