from cards import views as card_views

from cardsets import views as cardset_views

from pokemons import views as pokemon_views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cards', card_views.CardViewSet, basename="card")
router.register(r'pokemons', pokemon_views.PokemonViewSet, basename="pokemon")
router.register(r'cardsets', cardset_views.CardSetViewSet, basename="cardset")
