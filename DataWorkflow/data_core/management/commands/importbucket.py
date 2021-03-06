# This code is modified from Pina Estany, Carles, & Thomas, Jenny. (2019, August 5). Swiss-Polar-Institute/science-cruise-data-management v0.1.0 (Version 0.1.0). Zenodo. http://doi.org/10.5281/zenodo.3360649
# Also available at: https://github.com/Swiss-Polar-Institute/science-cruise-data-management

from django.core.management.base import BaseCommand

from data_core.models import Bucket, Endpoint
import csv

class Command(BaseCommand):
    help = 'Adds lists of files from list in csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        print(options['filename'])
        self.import_data_from_csv(options['filename'])

    def import_data_from_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                endpoint, created = Endpoint.objects.get_or_create(name=row['endpoint'])

                bucket = Bucket()
                bucket.friendly_name = row['friendly_name']
                bucket.endpoint = endpoint
                bucket.name = row['name']

                bucket.save()