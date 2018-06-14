import os
import django

# used to execute this file without django running
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokepare.settings")
django.setup()

from cards.models import Card


cards = [{"name": "Pikachu", "description": "This is Pikachu!", "url": "www.test.com"}, {"name": "Evoli", "description": "This is Evoli!", "url": "www.test.com"}]


def fill_cards(model, cards_list):
    print("Feeding {}...".format(cards_list))

    for card in cards_list:
        model.objects.get_or_create(name=card["name"], description=card["description"])

    print("{} fed.".format(cards_list))


fill_cards(Card, cards)
