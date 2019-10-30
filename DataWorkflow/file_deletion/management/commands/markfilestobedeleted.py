from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted, Batch, MarkFilesDeleteCommand
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

    def check_deletion_will_not_make_lost_file(self, files_to_be_deleted):
        ids_to_be_deleted = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__id', flat=True)

        for file in files_to_be_deleted:
            qs = File.objects.filter(bucket__friendly_name=self._friendly_bucket_name).\
                exclude(id=file.id).\
                exclude(id__in=ids_to_be_deleted).\
                filter(etag=file.etag)

            if not qs.exists():
                cprint('File {} will be lost {}'.format(file.object_storage_key, file.etag), 'red')

    def check_deletion_will_not_make_lost_file2(self, files_to_be_deleted):
        file_ids_deleted = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__id', flat=True)

        file_ids_to_be_deleted = files_to_be_deleted.values_list('id', flat=True)

        etags_to_be_deleted = files_to_be_deleted.values_list('etag', flat=True)

        qs = File.objects.filter(bucket__friendly_name=self._friendly_bucket_name).\
            exclude(id__in=file_ids_deleted).\
            exclude(id__in=file_ids_to_be_deleted).\
            filter(etag__in=etags_to_be_deleted).\
            values_list('etag', flat=True)

        for etag_to_be_deleted in etags_to_be_deleted:
            if etag_to_be_deleted not in qs:
                files = File.objects.filter(bucket__friendly_name=self._friendly_bucket_name).\
                            exclude(id__in=file_ids_deleted).\
                            filter(etag=etag_to_be_deleted)

                for file in files:
                    print('Missing file:', file.object_storage_key, file.etag)

    def mark(self):
        deleted_ids = FileToBeDeleted.objects. \
            filter(file__bucket__friendly_name=self._friendly_bucket_name). \
            values_list('file__id', flat=True)

        files_to_be_deleted = File.objects.\
            filter(object_storage_key__startswith=self._object_storage_key_stargs_with).\
            filter(bucket__friendly_name=self._friendly_bucket_name).\
            exclude(id__in=deleted_ids)
        print('This file is going to be added for deletion:')

        for file in files_to_be_deleted:
            cprint(file.object_storage_key, 'green')

        self.check_deletion_will_not_make_lost_file(files_to_be_deleted)

        print('Total number of files to be added for deletion:', files_to_be_deleted.count())
        print('Do you want to continue? (Yy)')
        want_to_add_for_deleted = input()

        if want_to_add_for_deleted.lower() != 'y':
            exit(1)

        with transaction.atomic():
            # create an entry in the Batch table, which is just an id (primary key, so this is an auto-incrementing integer)
            batch = Batch()
            batch.save()

            mark_files_delete_command = MarkFilesDeleteCommand()
            mark_files_delete_command.batch = batch
            mark_files_delete_command.command = self._object_storage_key_stargs_with
            mark_files_delete_command.save()

            for file in files_to_be_deleted:
                file_to_be_deleted = FileToBeDeleted()
                file_to_be_deleted.batch = batch
                file_to_be_deleted.file = file
                file_to_be_deleted.save()

        cprint('Batch number of file(s) added for deletion: ' + str(batch), 'red')