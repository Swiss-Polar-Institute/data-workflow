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
        return File.objects.filter(etag=etag).exclude(id__in=self._files_to_be_deleted_ids).count() == 0

    def verify(self):
        print('Reading IDs for the files to be deleted for the bucket')
        self._files_to_be_deleted_ids = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__id', flat=True)


        print('Reading all the non-deleted etags for the bucket')
        etags_existing_for_bucket = set(File.objects.\
            filter(bucket__friendly_name=self._friendly_bucket_name).\
            exclude(id__in=self._files_to_be_deleted_ids).\
            values_list('etag', flat=True))

        etags_to_be_deleted = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__etag', flat=True)

        print('Checking files...')
        for etag_to_be_deleted in etags_to_be_deleted:
            if etag_to_be_deleted not in etags_existing_for_bucket:
                print('Warning file will be lost:')
                for file in File.objects.filter(bucket__friendly_name=self._friendly_bucket_name).filter(etag=etag_to_be_deleted):
                    print(file.object_storage_key)
