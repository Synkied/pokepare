from django.db import models

from pokepare.utils import OverwriteStorage

# Create your models here.


class HasLanguage(models.Model):

    language = models.ForeignKey(
        "Language",
        blank=True,
        null=True,
        related_name="%(class)s_language",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasName(models.Model):

    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        abstract = True


class HasPokemon(models.Model):

    pokemon = models.ForeignKey(
        "Pokemon",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class IsName(HasName, HasLanguage):
    class Meta:
        abstract = True


class Language(HasName):

    iso639 = models.CharField(max_length=10)
    iso3166 = models.CharField(max_length=2)
    official = models.BooleanField(default=False)


class LanguageName(IsName):

    local_language = models.ForeignKey(
        "Language",
        blank=True,
        null=True,
        related_name="locallanguage",
        on_delete=models.CASCADE,
    )


class Pokemon(HasName):

    height = models.IntegerField()
    weight = models.IntegerField()
    base_experience = models.IntegerField()
    is_default = models.BooleanField(default=False)


class PokemonSprites(HasPokemon):

    front_sprite = models.ImageField(
        storage=OverwriteStorage(),
        upload_to="pokemons/",
        blank=True,
        null=True,
    )
