from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted
from django.db.models import Max


class Command(BaseCommand):
    help = 'Mark files to be deleted'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)
        parser.add_argument('object_storage_key_starts_with', type=str)

    def handle(self, *args, **options):
        list_duplicated_files = MarkFilesToBeDeleted(options['friendly_bucket_name'],
                                                     options['object_storage_key_starts_with'])
        list_duplicated_files.mark()


class MarkFilesToBeDeleted:
    def __init__(self, friendly_bucket_name, object_storage_key_starts_with):
        self._friendly_bucket_name = friendly_bucket_name
        self._object_storage_key_stargs_with = object_storage_key_starts_with

    @staticmethod
    def get_deletion_batch_number():
        batch_number = FileToBeDeleted.objects.aggregate(Max('batch'))['batch__max']

        return batch_number+1 if batch_number else 1

    def mark(self):
        deleted_ids = FileToBeDeleted.objects. \
            filter(file__bucket__friendly_name=self._friendly_bucket_name). \
            values_list('file__id', flat=True)

        files_to_be_deleted = File.objects.\
            filter(object_storage_key__startswith=self._object_storage_key_stargs_with).\
            exclude(id__in=deleted_ids)

        print('It is going to add for deletion:')

        for file in files_to_be_deleted:
            print(file.object_storage_key)

        print('Total number of files to be added for deletion:', files_to_be_deleted.count())
        print('Do you want to continue? (Yy)')
        want_to_add_for_deleted = input()

        if want_to_add_for_deleted.lower() != 'y':
            exit(1)

        deletion_batch_number = MarkFilesToBeDeleted.get_deletion_batch_number()

        for file in files_to_be_deleted:
            files_to_be_deleted = FileToBeDeleted()
            files_to_be_deleted.batch = deletion_batch_number
            files_to_be_deleted.file = file
            files_to_be_deleted.save()
