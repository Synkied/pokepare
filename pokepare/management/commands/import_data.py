from math import ceil

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

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

        count = 0
        limit = 20

        url = 'http://pokeapi.co/api/v2/pokemon?limit=' + str(limit)

        res = requests.get(url)

        res_json = res.json()

        for _ in range(limit, ceil(int(res_json["count"]) / limit + 1)):
            # updating the url for the offset limit each turn

            res = requests.get(url)

            res_json = res.json()

            url = res_json["next"]
            print(url)
            res = requests.get(url)

            for index, pokemon in enumerate(res_json["results"]):
                count += 1

                pokemon = requests.get(res_json["results"][index]['url'])
                name = pokemon.json()['name'].title()
                pokemon_id = pokemon.json()['id']
                front_image = pokemon.json()['sprites']['front_default']

                my_pokemon = {
                    "name": name,
                    "number": pokemon_id,
                    "front_image": front_image,
                }

                pokemon_obj = Pokemon.objects.get_or_create(
                    **my_pokemon
                )
                self.stdout.write(self.style.WARNING(my_pokemon["name"] + ' imported...'))

        self.stdout.write(self.style.SUCCESS(str(count) + ' Pokemons imported!'))

    def import_cards(self):
        self.stdout.write(self.style.WARNING('Importing cards...'))

        url_tcg = 'https://api.pokemontcg.io/v1/cards?pageSize=1000'

        res_tcg = requests.get(url_tcg)

        cards = []

        for page in range(1, ceil(int(res_tcg.headers["Total-Count"]) / int(res_tcg.headers["Count"]) + 1)):

            url_tcg += ('&page=' + str(page))

            res_tcg = requests.get(url_tcg)
            res_tcg_json = res_tcg.json()["cards"]

            attributes_to_keep = ["name", "nationalPokedexNumber", "number", "types", "subtype", "supertype", "hp", "artist", "rarity", "series", "set", "setCode", "imageUrl"]
            keys_to_del = ["attacks", "imageUrlHiRes", "text", "weaknesses", "resistances", "retreatCost", "convertedRetreatCost", "ability", "evolvesFrom", "ancientTrait"]

            for index, card in enumerate(res_tcg_json):

                card["national_pokedex_number"] = card.pop("nationalPokedexNumber", None)
                card["unique_id"] = card.pop("id", None)
                card["number_in_set"] = card.pop("number", None)
                card["card_set"] = card.pop("set", None)
                card["card_set_code"] = card.pop("setCode", None)
                card["image_url"] = card.pop("imageUrl", None)

                if card["supertype"] == "Pokémon":
                    try:
                        card["pokemon"] = Pokemon.objects.get(name__icontains=card["name"]).id
                    except ObjectDoesNotExist as dneerr:
                        pass

                for arg in keys_to_del:
                    if arg in card:
                        card.pop(arg)

                cards.append(card)

            for card in cards:
                try:
                    my_card = Card.objects.create(
                        **card
                    )
                except ValueError as verr:
                    print("ValueError", verr, card["name"])

        self.stdout.write(self.style.SUCCESS(str(len(cards)) + ' cards imported!'))

    # def link_cards_pokemons(self):
    #     self.stdout.write(self.style.WARNING('Linking cards to pokemons...'))
    #     pass
    #     # url_poke = 'http://localhost:8000/api/pokemons/'
    #     # url_cards = "http://localhost:8000/api/cards/"
    #     # res_poke = requests.get(url_poke)
    #     # res_cards = requests.get(url_cards)
    #     # count = 0

    #     # pokemons = []

    #     # for index, pokemon in enumerate(res.json()["results"]):
    #     #     count += 1

    #     #     pokemon = requests.get(res.json()["results"][index]['url'])
    #     #     name = pokemon.json()['name'].title()
    #     #     pokemon_id = pokemon.json()['id']
    #     #     front_image = pokemon.json()['sprites']['front_default']

    #     #     pokemon = {
    #     #         "name": name,
    #     #         "number": pokemon_id,
    #     #         "front_image": front_image,
    #     #     }

    #     #     pokemons.append(pokemon)

    #     #     self.stdout.write(self.style.WARNING(name, 'fetched...'))

    #     # for pokemon in pokemons:
    #     #     my_pokemon = Pokemon.objects.create(
    #     #         **pokemon
    #     #     )
    #     #     self.stdout.write(self.style.WARNING(pokemon["name"], 'imported...'))
