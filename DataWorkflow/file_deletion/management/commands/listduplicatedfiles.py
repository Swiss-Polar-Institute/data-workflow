from django.core.management.base import BaseCommand

from data_core.models import File
from ...models import FileToBeDeleted
from django.db.models import Count


class Command(BaseCommand):
    help = 'List duplicated files'

    def add_arguments(self, parser):
        parser.add_argument('friendly_bucket_name', type=str)

    def handle(self, *args, **options):
        list_duplicated_files = ListDuplicatedFiles(options['friendly_bucket_name'])
        list_duplicated_files.list()


class ListDuplicatedFiles:
    def __init__(self, friendly_bucket_name):
        self._friendly_bucket_name = friendly_bucket_name

    def list(self):
        # select * from data_core_file where etag in (select distinct etag from data_core_file group by etag having count(*)>1) order by etag, object_storage_key;
        deleted_ids = FileToBeDeleted.objects.\
            filter(file__bucket__friendly_name=self._friendly_bucket_name).\
            values_list('file__id', flat=True)

        result = File.objects.\
            filter(bucket__friendly_name=self._friendly_bucket_name).\
            exclude(id__in=deleted_ids).values('etag', 'size').\
            annotate(number_of_files=Count('etag')).\
            filter(number_of_files__gt=1)

        total_number_files_duplicated = 0
        etags = []

        size_of_duplicated_files = 0
        for r in result:
            total_number_files_duplicated += r['number_of_files']
            etags.append(r['etag'])
            size_of_duplicated_files += r['size'] * (r['number_of_files']-1)

        print('Total number of files duplicated:', total_number_files_duplicated)

        files = File.objects.filter(etag__in=etags).order_by('etag')

        for file in files:
            print(file.object_storage_key.ljust(80), file.etag, str(file.size).rjust(10))

        print('Total number of files duplicated:', total_number_files_duplicated)
        print('Size of duplicated files: {:0.3f} GB'.format(size_of_duplicated_files/1024/1024/1024))
