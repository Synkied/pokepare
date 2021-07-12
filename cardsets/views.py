from cardsets.models import CardSet
from cardsets.serializers import CardSetSerializer

from django.shortcuts import render
from django.views import View

from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter


# Create your views here.


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


class CardSetView(View):

    template_name = "index.html"

    def get(self, request):

        cardsets = CardSet.objects.all()

        context = {
            "cardsets": cardsets,
        }

        return render(request, self.template_name, context)


class CardSetViewDetail(View):

    template_name = "index.html"

    def get(self, request, code):

        context = {}

        return render(request, self.template_name, context)
