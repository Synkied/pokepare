from django.db import models

from pokepare.utils import OverwriteStorage


#############################
#            HAS            #
#############################
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
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='%(class)s',
    )

    class Meta:
        abstract = True


class HasPokemonSpecies(models.Model):
    pokemon_species = models.ForeignKey(
        "PokemonSpecies",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


#############################
#            IS             #
#############################
class IsName(HasName, HasLanguage):
    class Meta:
        abstract = True


##############################
#          LANGUAGE          #
##############################
class Language(HasName):

    iso639 = models.CharField(max_length=10)
    iso3166 = models.CharField(max_length=2)
    official = models.BooleanField(default=False)


##############################
#           POKEMONS         #
##############################
class Pokemon(HasName, HasPokemonSpecies):
    number = models.PositiveIntegerField()
    front_sprite = models.ImageField(
        storage=OverwriteStorage(),
        upload_to="pokemons/",
        blank=True,
        null=True,
    )


class PokemonSpecies(HasName):
    pass


class PokemonSpeciesName(IsName, HasPokemonSpecies):
    pass


##############################
#           TYPES         #
##############################
class Type(HasName):
    pass
