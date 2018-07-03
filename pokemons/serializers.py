from rest_framework import serializers
from .models import Pokemon


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='pokemons:pokemon_detail',
        lookup_field='pk',
    )

    class Meta:
        model = Pokemon
        fields = '__all__'
