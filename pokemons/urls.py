from api.views.pokemon import PokemonListView
from api.views.pokemon import PokemonDetailView

from django.urls import path


app_name = "pokemons"

urlpatterns = [
    path('', PokemonListView.as_view(), name="pokemon_list"),
    path('<str:name>', PokemonDetailView.as_view(), name="pokemon_detail"),
]
