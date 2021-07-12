from django.shortcuts import render
from django.views import View

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from pokemons.models import Language
from pokemons.models import Pokemon
from pokemons.models import PokemonSpecies
from pokemons.models import PokemonSpeciesName

from rest_framework import permissions
from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Language
        fields = '__all__'


class LanguageDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Language
        fields = '__all__'


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    local_name = serializers.SerializerMethodField('get_local_name')

    def get_local_name(self, obj):
        query_language = self.context['request'].query_params.get(
            'language', None
        ) or 'en'

        if query_language:
            lang = Language.objects.get(name=query_language)
            local_name = PokemonSpeciesName.objects.get(
                language=lang,
                pokemon_species=obj.pokemon_species
            )
        return local_name.name

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    local_name = serializers.SerializerMethodField('get_local_name')

    def get_local_name(self, obj):
        query_language = self.context['request'].query_params.get(
            'language', None
        ) or 'en'

        if query_language:
            lang = Language.objects.get(name=query_language)
            local_name = PokemonSpeciesName.objects.get(
                language=lang,
                pokemon_species=obj.pokemon_species
            )
        return local_name.name

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonSpeciesNameSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ('name', 'language')


class PokemonSpeciesListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonSpecies
        fields = ('url', 'name')


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField('get_pokemon_names')
    evolves_from_species = PokemonSpeciesListSerializer()

    class Meta:
        model = PokemonSpecies
        fields = '__all__'

    def get_pokemon_names(self, obj):

        species_results = PokemonSpeciesName.objects.filter(
            pokemon_species=obj
        )
        species_serializer = PokemonSpeciesNameSerializer(
            species_results, many=True, context=self.context
        )

        data = species_serializer.data

        return data


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
        if self.action == 'list' and self.list_serializer_class is not None:
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
        fields = '__all__'


class PokemonFilter(FilterSet):
    insensitive_name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Pokemon
        exclude = ['front_sprite']
        fields = '__all__'


class PokemonSpeciesFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use 'exclude'
    insensitive_name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = PokemonSpecies
        fields = '__all__'


##############################
#           RESOURCES
##############################
class LanguageResource(PokePareCommonResource, ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Language.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    list_serializer_class = LanguageSerializer
    serializer_class = LanguageDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = LanguageFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['id']  # default ordering


class PokemonResource(PokePareCommonResource, ModelViewSet):
    """
    API endpoint that allows pokemons to be viewed or edited.
    """
    queryset = Pokemon.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    list_serializer_class = PokemonSerializer
    serializer_class = PokemonDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = PokemonFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['number']  # default ordering


class PokemonSpeciesResource(PokePareCommonResource, ModelViewSet):

    queryset = PokemonSpecies.objects.all().order_by('id')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    list_serializer_class = PokemonSpeciesListSerializer
    serializer_class = PokemonSpeciesDetailSerializer


class PokemonListView(View):
    template_name = "index.html"

    def get(self, request):
        pokemons = Pokemon.objects.all()
        context = {
            'pokemons': pokemons,
        }

        return render(request, self.template_name, context)


class PokemonDetailView(View):
    template_name = "index.html"

    def get(self, request, name):
        pokemon = Pokemon.objects.get(name=name)
        context = {
            'pokemon': pokemon,
        }

        return render(request, self.template_name, context)
