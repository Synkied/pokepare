from rest_framework import serializers
from .models import Set


class SetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='sets:set_detail',
        lookup_field='code',
    )

    class Meta:
        model = Set
        fields = '__all__'
