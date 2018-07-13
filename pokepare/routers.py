from rest_framework import routers
from cards import views as card_views
from pokemons import views as pokemon_views
from sets import views as set_views


router = routers.DefaultRouter()
router.register(r'cards', card_views.CardViewSet, base_name="card")
router.register(r'pokemons', pokemon_views.PokemonViewSet, base_name="pokemon")
router.register(r'sets', set_views.SetViewSet, base_name="set")
