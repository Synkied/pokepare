import functools
import operator
import re
import tempfile
import time
from math import ceil

from cards.models import Card
from cards.models import SubType

from cardsets.models import CardSet

from django.core import files
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.models import Q

from pokemons.models import Language
from pokemons.models import Pokemon
from pokemons.models import PokemonSpecies
from pokemons.models import PokemonSpeciesName

from pokepare.utils import deep_get

import requests

BASE_URL_TCG = 'https://api.pokemontcg.io/v2'


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
            self.clear_languages()
            self.clear_pokemons()
            self.clear_pokemon_species()
            self.clear_cards()
            self.clear_sets()
            self.import_languages()
            self.import_pokemons()
            self.import_cards()
            self.import_cardsets()
        elif import_type == 'languages':
            self.clear_languages()
            self.import_languages()
        elif import_type == 'pokemons':
            self.clear_pokemons()
            self.clear_pokemon_species()
            self.import_pokemons()
        elif import_type == 'clear_pokemons':
            self.clear_pokemons()
        elif import_type == 'cards':
            self.import_cards()
        elif import_type == 'cardsets':
            self.clear_sets()
            self.import_cardsets()
        elif import_type == 'clear':
            self.clear_pokemons()
            self.clear_sets()
            self.clear_cards()
        else:
            self.stdout.write(
                self.style.ERROR('Import argument not recognized! :('))

    def clear_pokemons(self):
        self.stdout.write(self.style.WARNING('Deleting all pokemons...'))
        Pokemon.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All pokemons deleted!'))

    def clear_pokemon_species(self):
        self.stdout.write(self.style.WARNING(
            'Deleting all pokemons species...'))
        PokemonSpecies.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All pokemons species deleted!'))

    def clear_languages(self):
        self.stdout.write(self.style.WARNING(
            'Deleting all languages...'))
        Language.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All languages deleted!'))

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
                    file_name = '-'.join((url.split('/')[-2::]))

                elif obj.__class__.__name__ == 'Pokemon':
                    ext = url.split('.')[-1]
                    file_name = '.'.join([str(obj.number), ext])

                elif obj.__class__.__name__ == 'CardSet':
                    file_name = '-'.join((url.split('/')[-2::]))

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
                if obj.__class__.__name__ == 'Pokemon':
                    obj.front_sprite.save(file_name, files.File(lf))
                else:
                    obj.image.save(file_name, files.File(lf))
        else:
            return False

    ##############################
    # Importing Pokemons
    ##############################
    def import_pokemon_species(self, pokemon_specie, log_file):
        pokemon_sp_entry, created = PokemonSpecies.objects.update_or_create(  # noqa
            **pokemon_specie
        )
        self.log_imported(
            created,
            pokemon_specie,
            'name',
            log_file
        )

        return pokemon_sp_entry, created

    def import_pokemon_species_names(self,
                                     local_name, pokemon_sp_entry, log_file):
        # import pokemon species names
        language = Language.objects.get(
            name=local_name['language']['name']
        )
        new_poke_name = {
            'name': local_name['name'],
            'language': language,
            'pokemon_species': pokemon_sp_entry
        }
        poke_sp_name, created = PokemonSpeciesName.objects.get_or_create(
            **new_poke_name
        )
        self.log_imported(
            created,
            new_poke_name,
            'name',
            log_file
        )

    def import_languages(self):
        self.stdout.write(self.style.WARNING('Importing languages...'))
        import_log_file = 'log_import_languages.txt'
        lang_url = 'https://pokeapi.co/api/v2/language/'
        local_languages_url = 'https://gist.githubusercontent.com/Synkied/134c208fba5fd3b4046b75a34eb19670/raw/af0e4d90132f004ca565ddc841268e8b3bb7bc16/languages.json'  # noqa
        language_sprite_url = 'https://www.countryflags.io/'
        res = requests.get(lang_url)
        res_json = res.json()
        while res_json:
            try:
                local_languages = requests.get(local_languages_url).json()
                languages = res_json.get('results')
                for language in languages:
                    language_data = requests.get(language['url']).json()
                    for local_lang in local_languages:
                        iso639 = language_data.get('iso639', '').split('-')[0]
                        local_code = local_lang.get('code', '')
                        if iso639 == local_code:
                            language_data['local_name'] = local_lang['native']

                    language_data['sprite'] = '%s%s%s' % (
                        language_sprite_url,
                        language_data['iso3166'],
                        '/flat/16.png'
                    )
                    del language_data['names']
                    del language_data['id']

                    language, created = Language.objects.get_or_create(
                        **language_data
                    )

                    self.log_imported(
                        created,
                        language_data,
                        'name',
                        import_log_file)

                res_json = res_json.get('next')
            except KeyError as kerr:
                self.stdout.write(
                    'KeyError',
                    kerr,
                    '. Check if there was a request throttle.'
                )
                pass

    def import_pokemons(self):
        self.stdout.write(self.style.WARNING('Importing pokemons...'))
        limit = 20
        date_format = time.strftime('%Y-%m-%d_%H:%M')

        url = 'https://pokeapi.co/api/v2/pokemon-species/?limit=%s' % limit
        pokemon_sprites_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'  # noqa
        import_log_file = 'log_import_pokemons.txt'

        res = requests.get(url)
        res_json = res.json()

        with open(import_log_file, 'w') as f:
            f.write('Import started at: ' + '{}'.format(date_format) + '\n')

        while res_json.get('next'):
            try:
                pokemons = res_json.get('results')

                for pokemon in pokemons:
                    poke_sp_res = requests.get(pokemon.get('url'))
                    poke_sp = poke_sp_res.json()
                    pokemon_id = poke_sp.get('id')
                    pokemon_front_sprite = '%s%s.png' % (
                        pokemon_sprites_url, pokemon_id
                    )
                    pokemon_names = poke_sp.get('names')
                    evolves_from_name = deep_get(
                        poke_sp, 'evolves_from_species.name'
                    )
                    pokemon_evol = None
                    if evolves_from_name:
                        pokemon_evol, created = PokemonSpecies.objects.get_or_create(  # noqa
                            name=evolves_from_name
                        )

                    # import pokemon specie
                    new_pokemon_sp = {
                        'name': pokemon['name'],
                        'evolves_from_species': pokemon_evol,
                    }
                    pokemon_sp_entry, created = self.import_pokemon_species(
                        new_pokemon_sp,
                        import_log_file,
                    )

                    new_pokemon = {
                        'number': pokemon_id,
                        'front_sprite': pokemon_front_sprite,
                        'pokemon_species': pokemon_sp_entry,
                        'name': pokemon['name']
                    }
                    pokemon_entry, created = Pokemon.objects.get_or_create(
                        **new_pokemon
                    )
                    self.log_imported(
                        created,
                        new_pokemon,
                        'number',
                        import_log_file
                    )

                    for local_name in pokemon_names:
                        self.import_pokemon_species_names(
                            local_name,
                            pokemon_sp_entry,
                            import_log_file
                        )

                    self.get_remote_image(pokemon_front_sprite, pokemon_entry)

                page_res = requests.get(res_json['next'])
                res_json = page_res.json()
            except KeyError as kerr:
                self.stdout.write(
                    'KeyError',
                    kerr,
                    '. Check if there was a request throttle.'
                )
                pass

        with open(import_log_file, 'a') as f:
            f.write('Import finished at: ' + '{}'.format(date_format))

        self.stdout.write(
            self.style.SUCCESS(
                str(Pokemon.objects.count()) + ' Pokemons imported!'))

##############################
# Importing cards
##############################
    def import_subtypes(self):
        self.stdout.write('Importing subtypes...')
        headers = {'X-Api-Key': '0942fc67-dc0a-41f5-9c6d-8d46817f9a3d'}
        url_tcg_subtypes = '%s/subtypes' % (BASE_URL_TCG)
        res_tcg_subtypes = requests.get(url_tcg_subtypes, headers=headers)

        res_tcg_subtypes_json = res_tcg_subtypes.json()
        for subtype in res_tcg_subtypes_json['data']:
            _, created = SubType.objects.get_or_create(
                name=subtype
            )
            if created:
                self.stdout.write(subtype + ' imported...')

    def import_cards(self):
        self.import_subtypes()
        self.stdout.write('Importing cards...')
        headers = {'X-Api-Key': '0942fc67-dc0a-41f5-9c6d-8d46817f9a3d'}
        url_tcg_cards = '%s/cards' % (BASE_URL_TCG)
        res_tcg_cards = requests.get(url_tcg_cards, headers=headers)

        cards = []
        res_tcg_cards_json = res_tcg_cards.json()
        total_count = res_tcg_cards_json["totalCount"]
        current_count = res_tcg_cards_json["count"]
        count = ceil(int(total_count) // int(current_count)) + 2

        for page in range(1, count):
            print("Fetching from: ", url_tcg_cards)
            res_tcg_cards = requests.get(url_tcg_cards, headers=headers)
            res_tcg_cards_json = res_tcg_cards.json()
            datas = res_tcg_cards_json['data']
            current_count = res_tcg_cards_json["count"]

            try:
                url_tcg_cards = '%s/cards?page=%s' % (BASE_URL_TCG, page)
            except KeyError:
                pass

            # attributes_to_keep = ['name', 'nationalPokedexNumber', 'number', 'types', 'subtype', 'supertype', 'hp', 'artist', 'rarity', 'series', 'set', 'setCode', 'imageUrl']
            keys_to_del = [
                "attacks",
                "abilities",
                "legalities",
                "imageUrlHiRes",
                "text",
                "level",
                "weaknesses",
                "resistances",
                "retreatCost",
                "convertedRetreatCost",
                "ability",
                "evolvesFrom",
                "evolvesTo",
                "ancientTrait",
                "tcgplayer",
                "flavorText",
                "rules",
            ]

            for index, card in enumerate(datas):
                pokedex_numbers = card.pop(
                    "nationalPokedexNumbers", None
                )
                if pokedex_numbers:
                    card["national_pokedex_number"] = pokedex_numbers[0]
                card["unique_id"] = card.pop("id", None)
                card["number_in_set"] = card.pop("number", None)

                # card set
                card["card_set"] = deep_get(card, 'set.name')
                card["series"] = deep_get(card, 'set.series')
                set_id = deep_get(card, 'set.id')
                card["card_set_code"] = set_id
                card.pop('set', None)

                image_url = deep_get(card, 'images.small')
                card["image_url"] = image_url
                card.pop('images', None)
                card['subtypes'] = set()
                for subtype in card['subtypes']:
                    subtype = SubType.objects.get(name=subtype)
                    card['subtypes'].add(subtype)
                card.pop('subtypes', None)

                if card['supertype'] == 'Pokémon':
                    # link cards and pokemons together using Q objects
                    # We split the name of the pokemon's card and
                    # we then search for each of the terms in the card's name
                    # the query only links to pokemons, as other terms
                    # like 'EX' are not pokemon objects
                    try:
                        q = re.split(r"[\W+|_']+", card['name'])
                        # remove chars between words, including '_'
                        query = functools.reduce(
                            operator.or_, (
                                Q(
                                    name__iexact=item
                                ) for item in q if len(item) > 1)
                            # if to not include unown with other cards
                        )
                        card['pokemon'] = Pokemon.objects.filter(
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
                self.get_remote_image(card['image_url'], my_card)

                self.stdout.write(card['name'] + ' imported...')
            except ValueError as verr:
                print('ValueError', verr, card['name'])

        self.stdout.write(
            self.style.SUCCESS(str(len(cards)) + ' cards imported!')
        )

##############################
# Importing sets
##############################
    def import_cardsets(self):
        self.stdout.write('Importing cardsets...')
        url_tcg = '%s/sets' % (BASE_URL_TCG)
        res_tcg = requests.get(url_tcg)
        res_tcg_json = res_tcg.json()

        card_sets = []
        total_count = res_tcg_json["totalCount"]
        current_count = res_tcg_json["count"]
        count = ceil(int(total_count) // int(current_count)) + 2

        for page in range(1, count):
            print("Fetching from: ", url_tcg)
            res_tcg = requests.get(url_tcg)
            res_tcg_json = res_tcg.json()
            datas = res_tcg_json['data']

            try:
                url_tcg = '%s/sets?page=%s' % (BASE_URL_TCG, page)
            except KeyError:
                pass

            keys_to_del = [
                "legalities",
                "expandedLegal",
                "updatedAt",
                "updatedSince",
                "pageSize",
                "ptcgoCode",
                "printedTotal",
            ]

            for index, card_set in enumerate(datas):
                card_set["release_date"] = card_set.pop("releaseDate", None)
                card_set["total_cards"] = card_set.pop("total", None)
                images = card_set['images']
                card_set["logo_url"] = images['logo']
                card_set["symbol_url"] = images['symbol']
                card_set['code'] = card_set.pop('id')
                card_set.pop('images')

                for arg in keys_to_del:
                    if arg in card_set:
                        card_set.pop(arg)

                card_sets.append(card_set)

        for card_set in card_sets:
            try:
                my_card_set, created = CardSet.objects.get_or_create(
                    **card_set
                )
                self.get_remote_image(card_set['logo_url'], my_card_set)

                self.stdout.write(card_set['name'] + ' imported...')
            except ValueError as verr:
                print('ValueError', verr, card_set['name'])

        self.stdout.write(
            self.style.SUCCESS(str(len(card_sets)) + ' sets imported!'))

    def log_imported(self, created, obj, key, log_file):
        if created:
            self.stdout.write('%s %s' % (
                    obj[key], 'imported...\n'))
            with open(log_file, 'a') as f:
                f.write('%s %s' % (
                    obj[key], 'imported...\n'))
        else:
            self.stdout.write('%s %s' % (
                obj[key], 'NOT CREATED...'))
            with open(log_file, 'a') as f:
                f.write('%s %s' % (
                    obj[key], 'NOT CREATED...'))
