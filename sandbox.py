import os
import django
import re
import functools
import operator

# used to execute this file without django running
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokepare.settings")
django.setup()


from pokemons.models import Pokemon
from cards.models import Card
from django.db.models import Q


card = Card.objects.get(name="Erika's Ivysaur")

q = re.split(r"[\W+|_']+", card.name)
# remove chars between words, including "_"
query = functools.reduce(
    operator.or_, (
        Q(
            name__iexact=item
        ) for item in q if len(item) > 1)
    # if to not include unown with other cards
)

pok = Pokemon.objects.filter(query).order_by('id').first()
print(pok.name)
