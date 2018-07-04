from django.core.management.base import BaseCommand

import requests
from pokemons.models import Pokemon


class Command(BaseCommand):
    help = 'Import data from pokeapi API'

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
            self.clear_pokemons()
            self.import_pokemons()
        else:
            self.stdout.write(self.style.ERROR('Import argument not recognized! :('))

    def clear_pokemons(self):
        self.stdout.write(self.style.WARNING('Deleting all pokemons...'))
        Pokemon.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All pokemons deleted!'))

    def import_pokemons(self):
        url = 'http://pokeapi.co/api/v2/pokemon?limit=1'

        res = requests.get(url)

        print(res.json())

        pokemon = requests.get(res.json()["results"][0]['url'])
        name = pokemon.json()['name'].title()
        pokemon_id = pokemon.json()['id']
        front_image = pokemon.json()['sprites']['front_default']

        my_pokemon = Pokemon.objects.create(
            name=name,
            id=pokemon_id,
            front_image=front_image
        )

        print(name, pokemon_id, front_image)
