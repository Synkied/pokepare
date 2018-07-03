from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    pokemon = serializers.HyperlinkedRelatedField(view_name='pokemons:pokemon_detail', read_only=True, lookup_field='name')
    url = serializers.HyperlinkedIdentityField(
        view_name='cards:card_detail',
        lookup_field='name',
    )

    class Meta:
        model = Card
        fields = '__all__'
