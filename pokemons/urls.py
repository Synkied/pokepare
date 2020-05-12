from django.urls import path

from . import views

app_name = "pokemons"

urlpatterns = [
    path('', views.PokemonView.as_view(), name="pokemon_list"),
    path(
        '<str:name>',
        views.PokemonTranslationViewDetail.as_view(),
        name="pokemon_translation_detail"
    ),
    path(
        '<str:number>',
        views.PokemonViewDetail.as_view(),
        name="pokemon_detail"
    ),
]
