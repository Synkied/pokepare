import functools
import operator
import re
import tempfile
import time
from math import ceil

from cards.models import Card

from cardsets.models import CardSet

from django.core import files
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.models import Q

from pokemons.models import Pokemon

import requests


class Command(BaseCommand):
    help = 'Import data from pokeapi API'

    def add_arguments(self, parser):
        parser.add_argument('import_type', type=str, nargs='?', default='all')

    def handle(self, *args, **options):
        import_type = options.get('import_type', None)

        if import_type:
            self.stdout.write(self.style.WARNING('Starting import'))
        else:
            self.stdout.write(
                self.style.ERROR('Importing failed. Check arguments.'))
            return False

        if import_type == 'all':
            self.clear_pokemons()
            self.clear_cards()
            self.clear_sets()
            self.import_pokemons()
            self.import_cards()
            self.import_sets()
        elif import_type == 'pokemons':
            self.clear_pokemons()
            self.import_pokemons()
        elif import_type == 'cards':
            self.clear_cards()
            self.import_cards()
        elif import_type == 'sets':
            self.clear_sets()
            self.import_sets()
        elif import_type == 'clear':
            self.clear_pokemons()
            self.clear_cards()
        else:
            self.stdout.write(
                self.style.ERROR('Import argument not recognized! :('))

    def clear_pokemons(self):
        self.stdout.write(self.style.WARNING('Deleting all pokemons...'))
        Pokemon.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All pokemons deleted!'))

    def clear_cards(self):
        self.stdout.write(self.style.WARNING('Deleting all cards...'))
        Card.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All cards deleted!'))

    def clear_sets(self):
        self.stdout.write(self.style.WARNING('Deleting all sets...'))
        CardSet.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All sets deleted!'))

    def get_remote_image(self, url, obj):

        if url:
            request = requests.get(url, stream=True)

            if request.status_code == 200:
                if obj.__class__.__name__ == 'Card':
                    file_name = "-".join((url.split('/')[-2::]))

                elif obj.__class__.__name__ == 'Pokemon':
                    file_name = ".".join([obj.name, url.split('.')[-1]])

                elif obj.__class__.__name__ == 'CardSet':
                    file_name = "-".join((url.split('/')[-2::]))

                else:
                    return False

                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in request.iter_content(1024 * 8):

                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)

                obj.image.save(file_name, files.File(lf))
        else:
            return False

##############################
# Importing Pokemons
##############################
    def import_pokemons(self):
        self.stdout.write(self.style.WARNING('Importing pokemons...'))

        count = 0
        limit = 20
        date_format = time.strftime('%Y-%m-%d_%H:%M')

        url = 'http://pokeapi.co/api/v2/pokemon?limit=' + str(limit)

        res = requests.get(url)

        res_json = res.json()

        with open("log_import_pokemons" + ".txt", 'w') as f:
            f.write("Import started at: " + "{}".format(date_format) + '\n')

        while res_json.get('next'):
            try:
                page_res = requests.get(res_json['next'])
                pokemons = res_json.get('results')

                for index, pokemon in enumerate(pokemons):
                    count += 1

                    new_pokemon = requests.get(
                        res_json["results"][index]['url'])
                    name = new_pokemon.json()['name'].title()
                    pokemon_id = new_pokemon.json()['id']
                    image = new_pokemon.json()['sprites']['front_default']

                    my_pokemon = {
                        "name": name,
                        "number": pokemon_id,
                        "image": image,
                    }

                    pokemon_obj, created = Pokemon.objects.get_or_create(
                        **my_pokemon
                    )
                    self.get_remote_image(image, pokemon_obj)

                    if created:
                        self.stdout.write(my_pokemon["name"] + ' imported...')
                        with open("log_import_pokemons" + ".txt", 'a') as f:
                            f.write(my_pokemon["name"] + ' imported... \n')
                    else:
                        self.stdout.write(
                            my_pokemon["name"] + ' NOT CREATED...')
                        with open("log_import_pokemons" + ".txt", 'a') as f:
                            f.write(my_pokemon["name"] + ' imported... \n')

                res_json = page_res.json()
            except KeyError as kerr:
                self.stdout.write(
                    "KeyError",
                    kerr,
                    ". Check if there was a request throttle."
                )
                pass

        with open("log_import_pokemons" + ".txt", 'a') as f:
            f.write("Import finished at: " + "{}".format(date_format))

        self.stdout.write(
            self.style.SUCCESS(str(count) + ' Pokemons imported!'))

##############################
# Importing cards
##############################
    def import_cards(self):
        self.stdout.write('Importing cards...')

        url_tcg = 'https://api.pokemontcg.io/v1/cards?pageSize=1000'

        res_tcg = requests.get(url_tcg)

        cards = []
        total_count = res_tcg.headers["Total-Count"]
        current_count = res_tcg.headers["Count"]
        count = ceil(int(total_count) // int(current_count)) + 1

        for _ in range(count):

            print("Fetching from: ", url_tcg)

            res_tcg = requests.get(url_tcg)

            res_tcg_json = res_tcg.json()["cards"]

            try:
                url_tcg = res_tcg.links["next"]["url"]
            except KeyError:
                pass

            # attributes_to_keep = ["name", "nationalPokedexNumber", "number", "types", "subtype", "supertype", "hp", "artist", "rarity", "series", "set", "setCode", "imageUrl"]
            keys_to_del = [
                "attacks",
                "imageUrlHiRes",
                "text",
                "weaknesses",
                "resistances",
                "retreatCost",
                "convertedRetreatCost",
                "ability",
                "evolvesFrom",
                "ancientTrait",
            ]

            for index, card in enumerate(res_tcg_json):

                card["national_pokedex_number"] = card.pop(
                    "nationalPokedexNumber", None)
                card["unique_id"] = card.pop("id", None)
                card["number_in_set"] = card.pop("number", None)
                card["card_set"] = card.pop("set", None)
                card["card_set_code"] = card.pop("setCode", None)
                card["image_url"] = card.pop("imageUrl", None)

                if card["supertype"] == "Pokémon":
                    # link cards and pokemons together using Q objects
                    # We split the name of the pokemon's card and
                    # we then search for each of the terms in the card's name
                    # the query only links to pokemons, as other terms
                    # like "EX" are not pokemon objects
                    try:
                        q = re.split(r"[\W+|_']+", card["name"])
                        # remove chars between words, including "_"
                        query = functools.reduce(
                            operator.or_, (
                                Q(
                                    name__iexact=item
                                ) for item in q if len(item) > 1)
                            # if to not include unown with other cards
                        )
                        card["pokemon"] = Pokemon.objects.filter(
                            query).order_by('id').first()

                    except ObjectDoesNotExist:
                        pass

                for arg in keys_to_del:
                    if arg in card:
                        card.pop(arg)

                cards.append(card)

        for card in cards:
            try:
                my_card, created = Card.objects.get_or_create(
                    **card
                )
                self.get_remote_image(card["image_url"], my_card)

                self.stdout.write(card["name"] + ' imported...')
            except ValueError as verr:
                print("ValueError", verr, card["name"])

        self.stdout.write(
            self.style.SUCCESS(str(len(cards)) + ' cards imported!')
        )

##############################
# Importing sets
##############################
    def import_sets(self):
        self.stdout.write('Importing sets...')

        url_tcg = 'https://api.pokemontcg.io/v1/sets?pageSize=100'

        res_tcg = requests.get(url_tcg)

        card_sets = []
        total_count = res_tcg.headers["Total-Count"]
        current_count = res_tcg.headers["Count"]
        count = ceil(int(total_count) // int(current_count)) + 1

        for _ in range(count):

            print("Fetching from: ", url_tcg)

            res_tcg = requests.get(url_tcg)

            res_tcg_json = res_tcg.json()["sets"]

            try:
                url_tcg = res_tcg.links["next"]["url"]
            except KeyError:
                pass

            # attributes_to_keep = ["name", "nationalPokedexNumber", "number", "types", "subtype", "supertype", "hp", "artist", "rarity", "series", "set", "setCode", "imageUrl"]
            keys_to_del = [
                "standardLegal",
                "expandedLegal",
                "updatedAt",
                "updatedSince",
                "pageSize",
                "ptcgoCode",
            ]

            for index, card_set in enumerate(res_tcg_json):

                card_set["release_date"] = card_set.pop("releaseDate", None)
                card_set["total_cards"] = card_set.pop("totalCards", None)
                card_set["logo_url"] = card_set.pop("logoUrl", None)
                card_set["symbol_url"] = card_set.pop("symbolUrl", None)

                for arg in keys_to_del:
                    if arg in card_set:
                        card_set.pop(arg)

                card_sets.append(card_set)

        for card_set in card_sets:
            try:
                my_card_set, created = CardSet.objects.get_or_create(
                    **card_set
                )
                self.get_remote_image(card_set["logo_url"], my_card_set)

                self.stdout.write(card_set["name"] + ' imported...')
            except ValueError as verr:
                print("ValueError", verr, card_set["name"])

        self.stdout.write(
            self.style.SUCCESS(str(len(card_sets)) + ' sets imported!'))
