from cards.models import Card

from django.shortcuts import render
from django.views import View

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Pokemon
from .models import PokemonTranslation
from .serializers import PokemonSerializer

# Create your views here.


class PokemonFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    insensitive_name = filters.CharFilter(
        field_name="name",
        lookup_expr='icontains'
    )

    class Meta:
        model = Pokemon
        exclude = ['front_sprite']
        fields = '__all__'


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


class PokemonTranslationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = PokemonTranslation.objects.all()
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


class PokemonTranslationView(View):
    template_name = "index.html"

    def get(self, request):
        pokemons_trans = PokemonTranslation.objects.all()

        context = {
            "pokemons_trans": pokemons_trans,
        }

        return render(request, self.template_name, context)


class PokemonViewDetail(View):
    template_name = "index.html"

    def get(self, request, number):
        context = {}
        return render(request, self.template_name, context)


class PokemonTranslationViewDetail(View):
    template_name = "index.html"

    def get(self, request, name):
        pokemons_trans = PokemonTranslation.objects.get(name=name)
        context = {
            "pokemons_trans": pokemons_trans
        }
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
