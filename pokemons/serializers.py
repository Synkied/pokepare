from rest_framework import serializers

from .models import Language
from .models import Pokemon
from .models import PokemonSpecies
from .models import PokemonSpeciesName


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Language
        fields = "__all__"


class LanguageDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Language
        fields = "__all__"


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name="pokemons:pokemon_detail",
        lookup_field="number",
    )

    class Meta:
        model = Pokemon
        fields = "__all__"


class PokemonSpeciesNameSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ("name", "language")


class PokemonSpeciesListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonSpecies
        fields = ("url", "name")


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField("get_pokemon_names")

    class Meta:
        model = PokemonSpecies
        fields = "__all__"

    def get_pokemon_names(self, obj):

        species_results = PokemonSpeciesName.objects.filter(
            pokemon_species=obj)
        species_serializer = PokemonSpeciesNameSerializer(
            species_results, many=True, context=self.context
        )

        data = species_serializer.data

        return data
