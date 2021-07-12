from rest_framework import routers

from .views import card
from .views import cardset
from .views import pokemon

router = routers.DefaultRouter()
router.register(
    r'card',
    card.CardViewSet,
    basename="card",
)
router.register(
    r'cardset',
    cardset.CardSetViewSet,
    basename="cardset",
)
router.register(
    r'language',
    pokemon.LanguageResource,
    basename="language",
)
router.register(
    r'pokemon',
    pokemon.PokemonResource,
    basename="pokemon",
)
router.register(
    r'pokemonspecie',
    pokemon.PokemonSpeciesResource,
    basename="pokemonspecies",
)
