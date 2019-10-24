from django.db import models
from django.contrib.auth.models import User
import hashlib


class CreateModify(models.Model):
    """Details of data creation and modification: including date, time and user."""
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    created_on = models.DateTimeField(help_text='Date and time at which the entry was created', auto_now_add=True, blank=False, null=False)
    created_by = models.ForeignKey(User, help_text='User by which the entry was created', related_name="%(app_label)s_%(class)s_created_by_related", blank=True, null=True, on_delete=models.PROTECT)
    modified_on = models.DateTimeField(help_text='Date and time at which the entry was modified', auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, help_text='User by which the entry was modified', related_name="%(app_label)s_%(class)s_modified_by_related", blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Endpoint(CreateModify):
    """Details of endpoint (provider of object storage)"""
    name = models.CharField(help_text='Name of endpoint or service provider', max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Bucket(CreateModify):
    """Details of object storage bucket."""
    friendly_name = models.CharField(help_text='Friendly name of bucket', max_length=50, blank=False, null=False, unique=True)
    name = models.CharField(help_text='Bucket UUID name', max_length=50, blank=False, null=False, unique=True)
    endpoint = models.ForeignKey(Endpoint, help_text='Details of the endpoint of where the bucket is located', on_delete=models.PROTECT)

    def __str__(self):
        return "{}: {} - {}".format(self.friendly_name, self.name, self.endpoint)


class SourceFile(CreateModify):
    """Details of files that are used to import file lists"""
    name = models.CharField(help_text='Name of file', max_length=150, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class AbstractFile(CreateModify):
    """Abstract class to hold data about files that are held or were held in object storage buckets."""
    bucket = models.ForeignKey(Bucket, help_text='Details of the object storage bucket where the file is stored', blank=False, null=False, on_delete=models.PROTECT)
    object_storage_key = models.CharField(help_text='Object storage key of the file', max_length=1024, blank=False, null=False)
    filename = models.CharField(help_text='Filename', max_length=128, blank=False, null=False)
    etag = models.CharField(help_text='ETag of the file', max_length=36, blank=False, null=False)
    size = models.BigIntegerField(help_text='Size of the file in bytes', blank=False, null=False)
    source_file = models.ForeignKey(SourceFile, help_text='Name of source file from which the file was listed', on_delete=models.PROTECT)

    sha1_unique_together = models.CharField(max_length=40)

    def __str__(self):
        return "{} - {} {} {}".format(self.bucket, self.object_storage_key, self.etag, self.size)

    def calculate_sha1_unique_together(self):
        s = '{}{}{}'.format(self.bucket.id, self.object_storage_key, self.etag)
        s = s.encode('utf-8')

        return hashlib.sha1(s).hexdigest()

    def save(self, *args, **kwargs):
        self.sha1_unique_together = self.calculate_sha1_unique_together()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        unique_together = (('sha1_unique_together'), )


class File(AbstractFile):
    """Details about files that are held in object storage buckets."""
    pass


class BucketAdministration(CreateModify):
    """Details of buckets for purposes of administration."""
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS = (
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
    )
    bucket = models.OneToOneField(Bucket, help_text='Bucket to which these properties relate', on_delete=models.PROTECT)
    date_bucket_created = models.DateField(help_text='Date on which the bucket was created', blank=False, null=False)
    date_bucket_deleted = models.DateField(help_text='Date on which the bucket was removed')
    status = models.CharField(help_text='Status of the bucket', max_length=20, choices=STATUS, blank=False, null=False, default=ACTIVE)

    class Meta:
        verbose_name_plural = 'Bucket administration'