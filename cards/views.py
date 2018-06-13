from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class CardsView(View):
    template_name = "cards.html"

    def get(self, request):
        return render(request, self.template_name)
