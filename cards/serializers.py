from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Card
        fields = '__all__'
