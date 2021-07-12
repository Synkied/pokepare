from django.urls import path

from . import api

app_name = "pokemons"

urlpatterns = [
    path('', api.PokemonView.as_view(), name="pokemon_list"),
]
