from django.views import View
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import PokemonSerializer
from .models import Pokemon

# Create your views here.


class PokemonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'name'


class PokemonView(View):

    template_name = "pokemons.html"

    def get(self, request):

        pokemons = Pokemon.objects.all()

        context = {
            "pokemons": pokemons,
        }

        return render(request, self.template_name, context)


class PokemonViewDetail(View):

    template_name = "pokemons.html"

    def get(self, request, name):

        context = {
        }

        return render(request, self.template_name, context)
