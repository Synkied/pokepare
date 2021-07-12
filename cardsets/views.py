from cardsets.models import CardSet

from django.shortcuts import render
from django.views import View


class CardSetListView(View):

    template_name = "index.html"

    def get(self, request):

        cardsets = CardSet.objects.all()

        context = {
            "cardsets": cardsets,
        }

        return render(request, self.template_name, context)


class CardSetDetailView(View):

    template_name = "index.html"

    def get(self, request, code):

        context = {}

        return render(request, self.template_name, context)
