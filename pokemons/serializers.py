from rest_framework import serializers

from .models import Pokemon
from .models import PokemonTranslation


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='pokemons:pokemon_detail',
        lookup_field='number',
    )

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonTranslationSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='pokemons:pokemon_translation_detail',
        lookup_field='name',
    )

    class Meta:
        model = PokemonTranslation
        fields = '__all__'
