from cards.models import Card

from django.shortcuts import render
from django.views import View

from pokemons.models import Pokemon


class PokemonListView(View):

    template_name = "index.html"

    def get(self, request):

        pokemons = Pokemon.objects.all()

        context = {
            "pokemons": pokemons,
        }

        return render(request, self.template_name, context)


class PokemonViewDetail(View):

    template_name = "index.html"

    def get(self, request, name):

        context = {}

        return render(request, self.template_name, context)


class PokemonCardsViewDetail(View):

    template_name = "index.html"

    def get(self, request):
        # initial instantiation to avoid TypeError and empty card.prices
        cards = Card.objects.all()
        context = {
            "cards": cards,
        }

        return render(request, self.template_name, context)
