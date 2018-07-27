import os

from django.core.management.base import BaseCommand
from django.conf import settings

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


class Command(BaseCommand):
    help = 'Put images in elasticsearch'

    img_base_dir = settings.MEDIA_ROOT
    img_dir = img_base_dir + '/cards/'
    dirlist = os.listdir(img_dir)

    def add_arguments(self, parser):
        parser.add_argument('-import_type', type=str, nargs='?', default='all')
        parser.add_argument('-dir', type=str, nargs='?', default=self.img_dir)

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

    def add_to_es(self, img_dir=img_dir):

        es = Elasticsearch(hosts=[{"host": settings.ELASTICSEARCH_HOST}])
        ses = SignatureES(es, distance_cutoff=0.3)

        for file in self.dirlist:
            file_ext = "".join(file.split('.')[-1::])
            img_path = img_dir + file
            if file_ext in ('png', 'jpg'):
                print(img_path, 'added.')
                ses.add_image(img_path)
