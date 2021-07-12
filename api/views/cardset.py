from cardsets.models import CardSet

from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter


class CardSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='cardsets:cardset_detail',
        lookup_field='code',
    )

    class Meta:
        model = CardSet
        fields = '__all__'


class CardSetFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    class Meta:
        model = CardSet
        exclude = ['image']


class CardSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sets to be viewed or edited.
    """
    queryset = CardSet.objects.all()
    serializer_class = CardSetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = CardSetFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['release_date']  # default ordering
