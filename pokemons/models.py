from django.db import models

from pokepare.utils import OverwriteStorage

# Create your models here.


class Pokemon(models.Model):
    number = models.PositiveIntegerField()


class PokemonTranslations(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='pokemon_translations',
    )
    language = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    image = models.ImageField(
        storage=OverwriteStorage(),
        upload_to="pokemons/",
        blank=True,
        null=True,
    )
