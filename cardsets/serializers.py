from rest_framework import serializers

from .models import CardSet


class CardSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='cardsets:set_detail',
        lookup_field='code',
    )

    class Meta:
        model = CardSet
        fields = '__all__'
