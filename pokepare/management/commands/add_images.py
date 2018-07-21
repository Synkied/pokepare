import os

from django.core.management.base import BaseCommand
from django.conf import settings

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


class Command(BaseCommand):
    help = 'Put images in elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('import_type', type=str, nargs='?', default='all')

    def handle(self, *args, **options):
        import_type = options.get('import_type', None)

        if import_type:
            self.stdout.write(self.style.WARNING('Starting import'))
        else:
            self.stdout.write(self.style.ERROR('Importing failed. Check arguments.'))
            return False

        if import_type == 'all':
            # self.clear_es()
            self.add_to_es()
        elif import_type == 'clear':
            self.clear_es()
        else:
            self.stdout.write(self.style.ERROR('Import argument not recognized! :('))

    def add_to_es(self):

        es = Elasticsearch(hosts=[{"host": 'elasticsearch'}])
        ses = SignatureES(es, distance_cutoff=0.3)

        img_base_dir = settings.MEDIA_ROOT

        img_dir = img_base_dir + '/cards/'

        dirlist = os.listdir(img_dir)

        for file in dirlist:
            img_path = img_dir + file
            print(img_path, 'added.')
            ses.add_image(img_path)
