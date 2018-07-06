from django.db import models
from django.utils import timezone
from django.conf import settings

from pokemons.models import Pokemon

# Create your models here.


class Card(models.Model):
    name = models.CharField(
        help_text='The card name.',
        max_length=500
    )
    nationalPokedexNumber = models.PositiveIntegerField(
        help_text='The national pokedex number for a card that features a Pokémon supertype.',
        blank=True,
        null=True
    )
    number_in_set = models.CharField(
        help_text='The number of the card for the set it was released in. Found on the bottom right side of the card.',
        max_length=20,
        blank=True,
        null=True
    )
    types = models.CharField(
        help_text='The types of the card. These typically appear in the top right of card, and are denoted by energy symbol (ex. Fire, Fighting, Psychic, etc.)',
        max_length=100,
        blank=True,
        null=True
    )
    subtype = models.CharField(
        help_text='MEGA/BREAK/Supporter...',
        max_length=100,
        blank=True,
        null=True
    )
    supertype = models.CharField(
        help_text='Pokémon/Trainer/Energy',
        max_length=100,
        blank=True,
        null=True
    )
    hp = models.PositiveIntegerField(
        help_text='The number of the card for the set it was released in. Found on the bottom right side of the card.',
        blank=True,
        null=True
    )
    artist = models.CharField(
        help_text='The artist of the card.',
        max_length=200,
        blank=True,
        null=True
    )
    rarity = models.CharField(
        help_text="Common/Holo/Shining/Full Art...",
        max_length=50,
        blank=True,
        null=True
    )
    series = models.CharField(
        help_text='The series the card appears in (ex. Base, XY, EX, etc.)',
        max_length=50,
        blank=True,
        null=True
    )
    card_set = models.CharField(
        help_text='The set the card appears in (ex. BREAKthrough, Phantom Forces, Jungle, etc.)',
        max_length=100,
        blank=True,
        null=True
    )
    card_set_code = models.CharField(
        help_text='The unique code of the set (ex. base1, xy5, ex3)',
        max_length=20,
        blank=True,
        null=True
    )
    language = models.CharField(
        help_text='The language of the card.',
        max_length=5,
        blank=True,
        null=True
    )
    image = models.URLField(
        help_text='The front image of the card.',
        default=settings.CARD_PLACEHOLDER
    )
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='cards',
    )

    url = models.URLField(blank=True, null=True)

    condition = models.CharField(max_length=50, blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)

    image_hash = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)
