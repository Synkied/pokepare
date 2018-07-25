from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page


from . import views

app_name = "pokemons"

urlpatterns = [
    path('', cache_page(60 * 60)(views.PokemonView.as_view()), name="pokemon_list"),
    path('<str:name>', cache_page(60 * 60)(views.PokemonViewDetail.as_view()), name="pokemon_detail"),
]
