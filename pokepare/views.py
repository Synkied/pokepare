from cards.models import Card

from django.shortcuts import render
from django.views import View


# Create your views here.


class SearchView(View):

    template_name = "index.html"

    def get(self, request):

        search_query = request.GET.get('query')
        cards = Card.objects.filter(name__icontains=search_query)

        context = {
            'cards': cards,
        }

        return render(request, self.template_name, context)
