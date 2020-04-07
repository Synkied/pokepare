from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    pokemon = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='cards:card_detail',
        lookup_field='unique_id',
    )

    class Meta:
        model = Card
        fields = '__all__'
