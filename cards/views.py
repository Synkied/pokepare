import pprint

from django.views import View
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from .serializers import CardSerializer
from .models import Card
from sets.models import Set
from utils import PriceFinder


# Create your views here.


class CardFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut
    # but it won't let you use "exclude"
    insensitive_name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Card
        exclude = ['image']
        fields = ['insensitive_name', 'card_set_code', 'unique_id']


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = CardFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['national_pokedex_number']  # default ordering


class CardView(View):

    template_name = "index.html"

    def get(self, request):

        cards = Card.objects.all()

        context = {
            "cards": cards,
        }

        return render(request, self.template_name, context)


class CardViewDetail(View):

    template_name = "index.html"

    def get(self, request, unique_id):

        card = Card.objects.get(unique_id=unique_id)
        if card:
            card_set = Set.objects.get(code=card.card_set_code)

        context = {
            "card": card,
        }

        def retrieve_prices_data():

            # card_number_set = str(card.number_in_set + '/' + str(card_set.total_cards))
            price_finder = PriceFinder()
            ebay_cards = price_finder.get_ebay_prices(card.name, card.number_in_set, card_set.name)

            tcgplayer_cards = price_finder.get_tcgplayer_prices(card.name)

            for tcgplayer_card in tcgplayer_cards:
                if tcgplayer_card["group"]["name"] == card_set.name:
                    tcgplayer_cards = [tcgplayer_card]
                else:
                    tcgplayer_cards = ''

            # initial instantiation to avoid TypeError
            card.prices = {}

            card.prices["ebay"] = ebay_cards
            card.save()

            card.prices["tcgplayer"] = tcgplayer_cards
            card.save()
            print("Prices retrieved.")

            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(tcgplayer_cards)

        retrieve_prices_data()

        return render(request, self.template_name, context)
