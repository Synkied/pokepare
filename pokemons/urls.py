from django.urls import path

from . import views

app_name = "pokemons"

urlpatterns = [
    path('', views.PokemonView.as_view(), name="pokemon_list"),
    path('<str:name>', views.PokemonViewDetail.as_view(), name="pokemon_detail"),
]
