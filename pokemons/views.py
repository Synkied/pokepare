from cards.models import Card

from django.shortcuts import render
from django.views import View

from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Pokemon
from .serializers import PokemonSerializer

# Create your views here.


class PokemonFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    class Meta:
        model = Pokemon
        exclude = ['image']


class PokemonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PokemonFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['number']  # default ordering


class PokemonView(View):

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
        print('test')
        cards = Card.objects.all()
        context = {
            "cards": cards,
        }

        return render(request, self.template_name, context)
