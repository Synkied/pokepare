from math import ceil

from django.core.management.base import BaseCommand

import requests
from pokemons.models import Pokemon
from cards.models import Card


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
        elif import_type == 'pokemons':
            self.clear_pokemons()
            self.import_pokemons()
        elif import_type == 'cards':
            self.clear_cards()
            self.import_cards()
        elif import_type == 'clear':
            self.clear_pokemons()
            self.clear_cards()
        else:
            self.stdout.write(self.style.ERROR('Import argument not recognized! :('))

    def clear_pokemons(self):
        self.stdout.write(self.style.WARNING('Deleting all pokemons...'))
        Pokemon.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All pokemons deleted!'))

    def clear_cards(self):
        self.stdout.write(self.style.WARNING('Deleting all cards...'))
        Card.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All cards deleted!'))

    def import_pokemons(self):
        self.stdout.write(self.style.WARNING('Importing pokemons...'))

        url = 'http://pokeapi.co/api/v2/pokemon?limit=1000'
        res = requests.get(url)
        count = 0

        pokemons = []

        for index, pokemon in enumerate(res.json()["results"]):
            count += 1

            pokemon = requests.get(res.json()["results"][index]['url'])
            name = pokemon.json()['name'].title()
            pokemon_id = pokemon.json()['id']
            front_image = pokemon.json()['sprites']['front_default']

            pokemon = {
                "name": name,
                "number": pokemon_id,
                "front_image": front_image,
            }

            pokemons.append(pokemon)

        for pokemon in pokemons:
            my_pokemon = Pokemon.objects.create(
                **pokemon
            )

        self.stdout.write(self.style.SUCCESS(str(count) + ' Pokemons imported!'))

    def import_cards(self):
        self.stdout.write(self.style.WARNING('Importing cards...'))

        url_tcg = 'https://api.pokemontcg.io/v1/cards?pageSize=1000'
        count = 0

        res_tcg = requests.get(url_tcg)

        for page in range(1, ceil(int(res_tcg.headers["Total-Count"]) / int(res_tcg.headers["Count"]) + 1)):

            url_tcg += ('&page=' + str(page))

            res_tcg = requests.get(url_tcg)
            res_tcg_json = res_tcg.json()["cards"]

            attributes = ["name", "nationalPokedexNumber", "number", "types", "subtype", "supertype", "hp", "artist", "rarity", "series", "set", "setCode", "imageUrl"]

            cards = []

            for index, card in enumerate(res_tcg_json):
                count += 1

                try:
                    for attribute in attributes:
                        if attribute in res_tcg_json[index]:
                            name = res_tcg_json[index]["name"]
                            nationalPokedexNumber = res_tcg_json[index]["nationalPokedexNumber"]
                            number_in_set = res_tcg_json[index]["number"]
                            types = res_tcg_json[index]["types"]
                            subtype = res_tcg_json[index]["subtype"]
                            supertype = res_tcg_json[index]["supertype"]
                            hp = res_tcg_json[index]["hp"]
                            artist = res_tcg_json[index]["artist"]
                            rarity = res_tcg_json[index]["rarity"]
                            series = res_tcg_json[index]["series"]
                            card_set = res_tcg_json[index]["set"]
                            card_set_code = res_tcg_json[index]["setCode"]
                            image = res_tcg_json[index]["imageUrl"]

                except KeyError as kerr:
                    print('KeyError:', kerr, ' for', name)

                # if pokemon:
                #     pokemon = Pokemon.objects.get(name__icontains=name)

                card = {
                    "name": name,
                    "nationalPokedexNumber": nationalPokedexNumber,
                    "number_in_set": number_in_set,
                    "types": types,
                    "subtype": subtype,
                    "supertype": supertype,
                    "hp": hp,
                    "artist": artist,
                    "rarity": rarity,
                    "series": series,
                    "card_set": card_set,
                    "card_set_code": card_set_code,
                    "image": image,
                    # "pokemon": pokemon,
                }

                cards.append(card)

            for card in cards:
                my_card = Card.objects.create(
                    **card
                )

        self.stdout.write(self.style.SUCCESS(str(count) + ' cards imported!'))
