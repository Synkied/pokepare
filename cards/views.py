import pprint

from cards.models import Card
from cards.serializers import CardSerializer

from cardsets.models import CardSet

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from pokepare.utils import PriceFinder

from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

# Create your views here.


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
        # initial instantiation to avoid TypeError and empty card.prices
        card = Card.objects.get(unique_id=unique_id)

        if card:
            card_set = CardSet.objects.get(code=card.card_set_code)
            self.retrieve_prices_data(card, card_set)

        return render(request, self.template_name)

    def retrieve_prices_data(self, card, card_set):
        try:
            card.prices = []
            card.save()

            price_finder = PriceFinder()

            ebay_cards = price_finder.get_ebay_prices(
                card.name,
                card.number_in_set,
                card_set.name,
            )

            if ebay_cards:
                card.prices.extend(ebay_cards)

            tcgplayer_cards = price_finder.get_tcgplayer_prices(card.name)

            for tcgplayer_card in tcgplayer_cards:
                if tcgplayer_card["set_name"] == card_set.name:
                    tcgplayer_cards = [tcgplayer_card]
                    card.prices.extend(tcgplayer_cards)

                    print("tcgplayer")

            card.save()

            print("Prices retrieved.")

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(tcgplayer_cards)

        except ObjectDoesNotExist:
            pass
