from cards.serializers import CardSerializer

from rest_framework import serializers

from .models import Pokemon


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='pokemons:pokemon_detail',
        lookup_field='name',
    )
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = '__all__'
