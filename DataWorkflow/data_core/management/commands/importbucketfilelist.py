# This code is modified from Pina Estany, Carles, & Thomas, Jenny. (2019, August 5). Swiss-Polar-Institute/science-cruise-data-management v0.1.0 (Version 0.1.0). Zenodo. http://doi.org/10.5281/zenodo.3360649
# Also available at: https://github.com/Swiss-Polar-Institute/science-cruise-data-management

from django.core.management.base import BaseCommand

from data_core.models import File, Bucket, SourceFile
import csv
from data_core.progress_report import ProgressReport


class Command(BaseCommand):
    help = 'Adds lists of files from list in csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('friendly_bucket_name', type=str)

    def handle(self, *args, **options):
        print(options['filename'])
        self.import_data_from_csv(options['filename'], options['friendly_bucket_name'])

    @staticmethod
    def lines_of_file(filename):
        return sum(1 for line in open(filename))

    def import_data_from_csv(self, filename, friendly_bucket_name):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')

            bucket, created = Bucket.objects.get_or_create(friendly_name=friendly_bucket_name)
            source_file, created = SourceFile.objects.get_or_create(name=filename)

            to_be_inserted = []
            total_inserted = 0

            progress_report = ProgressReport(Command.lines_of_file(filename))

            for row in reader:
                file = File()
                file.object_storage_key = row[0]
                file.filename = row[0].split('/')[-1]
                file.size = row[1]
                file.etag = row[2]
                file.bucket = bucket
                file.source_file = source_file
                file.sha1_unique_together = file.calculate_sha1_unique_together()

                to_be_inserted.append(file)

                progress_report.increment_and_print_if_needed()

                if len(to_be_inserted) == 10000:
                    File.objects.bulk_create(to_be_inserted)
                    total_inserted += len(to_be_inserted)
                    print('Inserted ', total_inserted, 'files')

                    to_be_inserted = []

            File.objects.bulk_create(to_be_inserted)