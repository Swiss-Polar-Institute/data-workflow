from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted


class Command(BaseCommand):
    help = 'Output script to delete files from bucket'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)

    def handle(self, *args, **options):
        generate_script = GenerateScript(options['friendly_bucket_name'])
        generate_script.generate_script()


class GenerateScript:
    def __init__(self, friendly_bucket_name):
        self._friendly_bucket_name = friendly_bucket_name

    def generate_script(self):
        files_to_delete = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            order_by('file__object_storage_key')

        for file_to_delete in files_to_delete:
            print(f'rclone delete "{file_to_delete.file.object_storage_key}"')