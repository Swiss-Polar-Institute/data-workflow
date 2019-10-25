from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted


class Command(BaseCommand):
    help = 'Checks that no file has been deleted without having another copy'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)

    def handle(self, *args, **options):
        list_duplicated_files = VerifyFilesToBeDeleted(options['friendly_bucket_name'])
        list_duplicated_files.verify()


class VerifyFilesToBeDeleted:
    def __init__(self, friendly_bucket_name):
        self._friendly_bucket_name = friendly_bucket_name
        self._files_to_be_deleted_ids = None

    def all_copies_deleted(self, etag):
        return not File.objects.filter(etag=etag).exclude(id__in=self._files_to_be_deleted_ids).exists()

    def verify(self):
        self._files_to_be_deleted_ids = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__id', flat=True)

        files_to_be_deleted = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name)

        for file_to_be_deleted in files_to_be_deleted:
            file = file_to_be_deleted.file
            if self.all_copies_deleted(file.etag):
                print('Warning file will be lost:', file.object_storage_key)
