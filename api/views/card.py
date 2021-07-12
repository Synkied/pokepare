from cards.models import Card

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet


class CardFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    insensitive_name = filters.CharFilter(
        field_name="name",
        lookup_expr='icontains'
    )
    pokemon_id = filters.CharFilter(
        field_name="pokemon",
    )

    class Meta:
        model = Card
        exclude = ['image']
        fields = [
            'insensitive_name',
            'card_set_code',
            'unique_id',
            'pokemon_id'
        ]


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


class CardViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['national_pokedex_number']  # default ordering
    filter_class = CardFilter

    def get_queryset(self):
        qs = super(CardViewSet, self).get_queryset()
        qs = qs.select_related('pokemon')
        return qs
