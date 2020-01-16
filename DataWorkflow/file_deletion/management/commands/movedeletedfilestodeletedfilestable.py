from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted, DeletedFile
from django.db.models import Max
from django.forms.models import model_to_dict
from django.db import transaction

from data_core.progress_report import ProgressReport


class Command(BaseCommand):
    help = 'Moves deleted files to deleted files table'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)

    def handle(self, *args, **options):
        move_deleted_files_to_table = MoveFilesToDeletedFilesTable(options['friendly_bucket_name'])
        move_deleted_files_to_table.move()


class MoveFilesToDeletedFilesTable:
    def __init__(self, friendly_bucket_name):
        self._friendly_bucket_name = friendly_bucket_name

    def move(self):
        files_to_be_deleted = FileToBeDeleted.objects. \
            filter(file__bucket__friendly_name=self._friendly_bucket_name)

        progress_report = ProgressReport(files_to_be_deleted.count())

        with transaction.atomic():
            for file_to_be_deleted in files_to_be_deleted:
                deleted_file = DeletedFile()

                deleted_file.etag = file_to_be_deleted.file.etag
                deleted_file.object_storage_key = file_to_be_deleted.file.object_storage_key
                deleted_file.size = file_to_be_deleted.file.size
                deleted_file.bucket = file_to_be_deleted.file.bucket
                deleted_file.source_file = file_to_be_deleted.file.source_file

                deleted_file.save()
                file_to_be_deleted.delete()
                file_to_be_deleted.file.delete()

                progress_report.increment_and_print_if_needed()