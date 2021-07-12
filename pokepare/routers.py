from cards import views as card_views

from cardsets import views as cardset_views

from pokemons import api as pokemon_api

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'card', card_views.CardViewSet, basename="card")
router.register(r'cardset', cardset_views.CardSetViewSet, basename="cardset")
router.register(
    r'language', pokemon_api.LanguageResource, basename="language")
router.register(r'pokemon', pokemon_api.PokemonResource, basename="pokemon")
router.register(
    r'pokemonspecie',
    pokemon_api.PokemonSpeciesResource)
