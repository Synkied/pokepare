from rest_framework import routers
from cards import views as card_views
from pokemons import views as pokemon_views


router = routers.DefaultRouter()
router.register(r'cards', card_views.CardViewSet, base_name="cards")
router.register(r'pokemons', pokemon_views.PokemonViewSet, base_name="pokemons")
