import pprint

from cards.models import Card

from cardsets.models import CardSet

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from pokepare.utils import PriceFinder


class CardViewList(View):

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
