from django.shortcuts import render
from django.views import View

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Language
from .models import Pokemon
from .models import PokemonSpecies
from .serializers import LanguageDetailSerializer
from .serializers import LanguageSerializer
from .serializers import PokemonSerializer
from .serializers import PokemonSpeciesDetailSerializer
from .serializers import PokemonSpeciesListSerializer


##############################
#           GENERIC
##############################
class ListOrDetailSerialRelation:
    """
    Mixin to allow association with separate serializers
    for list or detail view.
    """

    list_serializer_class = None

    def get_serializer_class(self):
        if self.action == "list" and self.list_serializer_class is not None:
            return self.list_serializer_class
        return self.serializer_class


class PokePareCommonResource(ListOrDetailSerialRelation):
    pass


##############################
#           FILTERS
##############################
class LanguageFilter(FilterSet):
    class Meta:
        model = Language
        fields = "__all__"


class PokemonFilter(FilterSet):
    class Meta:
        model = Pokemon
        exclude = ["front_sprite"]
        fields = "__all__"


class PokemonSpeciesFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won"t let you use "exclude"
    insensitive_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = PokemonSpecies
        fields = "__all__"


##############################
#           RESOURCES
##############################
class LanguageResource(PokePareCommonResource, viewsets.ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Language.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    list_serializer_class = LanguageSerializer
    serializer_class = LanguageDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = LanguageFilter
    ordering_fields = "__all__"  # what field can be ordered via the API
    ordering = ["id"]  # default ordering


class PokemonResource(viewsets.ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Pokemon.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PokemonSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PokemonFilter
    ordering_fields = "__all__"  # what field can be ordered via the API
    ordering = ["number"]  # default ordering


class PokemonSpeciesResource(PokePareCommonResource, viewsets.ModelViewSet):

    queryset = PokemonSpecies.objects.all().order_by("id")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    list_serializer_class = PokemonSpeciesListSerializer
    serializer_class = PokemonSpeciesDetailSerializer


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

    def get(self, request, number):
        context = {}
        return render(request, self.template_name, context)
