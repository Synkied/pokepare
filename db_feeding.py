import os
import django

# used to execute this file without django running
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokepare.settings")
django.setup()

from pokemons.models import Pokemon
from cards.models import Card


pokemons = [{"name": "Pikachu"}, {"name": "Eevee"}]


def fill_pokemons(model, pokemons_list):
    print("Feeding {}...".format(pokemons_list))

    for pokemon in pokemons_list:
        model.objects.get_or_create(name=pokemon["name"])

    print("{} fed.".format(pokemons_list))


fill_pokemons(Pokemon, pokemons)


cards = [
    {
        "name": "Pikachu EX",
        "pokemon": Pokemon.objects.get(name="Pikachu"),
        "year": 2012,
        "version": 1,
    },
    {
        "name": "Ash's Pikachu",
        "pokemon": Pokemon.objects.get(name="Pikachu"),
        "year": 2014,
        "version": 1,
    },
    {
        "name": "Eevee EX",
        "pokemon": Pokemon.objects.get(name="Eevee"),
        "year": 2014,
        "version": 1,
    },
    {
        "name": "Eevee awesome",
        "pokemon": Pokemon.objects.get(name="Eevee"),
        "year": 2012,
        "version": 1,
    }
]


def fill_cards(model, cards_list):
    print("Feeding {}...".format(cards_list))

    for card in cards_list:
        model.objects.get_or_create(**card)

    print("{} fed.".format(cards_list))


fill_cards(Card, cards)
