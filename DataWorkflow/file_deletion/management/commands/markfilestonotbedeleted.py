from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileMarkedToNotBeDeleted, Batch, MarkFilesDeleteCommand
from django.db import transaction

from termcolor import cprint


class Command(BaseCommand):
    help = 'Mark files to NOT be deleted'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)
        parser.add_argument('object_storage_key_starts_with', type=str)

    def handle(self, *args, **options):
        list_duplicated_files = MarkFilesToNotBeDeleted(options['friendly_bucket_name'],
                                                        options['object_storage_key_starts_with'])
        list_duplicated_files.mark()


class MarkFilesToNotBeDeleted:
    def __init__(self, friendly_bucket_name, object_storage_key_starts_with):
        self._friendly_bucket_name = friendly_bucket_name
        self._object_storage_key_starts_with = object_storage_key_starts_with

    def mark(self):
        files_to_not_be_deleted = File.objects.\
            filter(object_storage_key__startswith=self._object_storage_key_starts_with).\
            filter(bucket__friendly_name=self._friendly_bucket_name)

        print('This file is going to be added for NOT deletion:')

        for file in files_to_not_be_deleted:
            cprint(file.object_storage_key, 'green')

        print('Total number of files to be added for NOT deletion:', files_to_not_be_deleted.count())
        print('Do you want to continue? (Yy)')
        want_to_add_for_deleted = input()

        if want_to_add_for_deleted.lower() != 'y':
            exit(1)

        with transaction.atomic(): # makes faster (only one save is done after all the operations below)
            # create an entry in the Batch table, which is just an id (primary key, so this is an auto-incrementing integer)
            batch = Batch()
            batch.save()

            mark_files_delete_command = MarkFilesDeleteCommand()
            mark_files_delete_command.batch = batch
            mark_files_delete_command.command = self._object_storage_key_starts_with
            mark_files_delete_command.save()

            for file in files_to_not_be_deleted:
                file_not_to_be_deleted = FileMarkedToNotBeDeleted()
                file_not_to_be_deleted.batch = batch
                file_not_to_be_deleted.file = file
                file_not_to_be_deleted.reason = FileMarkedToNotBeDeleted.REQUIRED_DUPLICATE
                file_not_to_be_deleted.save()

        cprint('Batch number of file(s) added for deletion: ' + str(batch), 'red')