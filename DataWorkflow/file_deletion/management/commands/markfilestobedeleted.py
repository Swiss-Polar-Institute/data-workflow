from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted
from django.db.models import Max
from django.db import transaction

from termcolor import cprint


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
        print('This file is going to be added for deletion:')

        for file in files_to_be_deleted:
            cprint(file.object_storage_key, 'green')

        print('Total number of files to be added for deletion:', files_to_be_deleted.count())
        print('Do you want to continue? (Yy)')
        want_to_add_for_deleted = input()

        if want_to_add_for_deleted.lower() != 'y':
            exit(1)

        deletion_batch_number = MarkFilesToBeDeleted.get_deletion_batch_number()

        with transaction.atomic():
            for file in files_to_be_deleted:
                file_to_be_deleted = FileToBeDeleted()
                file_to_be_deleted.batch = deletion_batch_number
                file_to_be_deleted.file = file
                file_to_be_deleted.save()

        cprint('Batch number of file(s) added for deletion: ' + str(deletion_batch_number), 'red')