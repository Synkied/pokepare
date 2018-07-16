from django.views import View
from django.shortcuts import render

# Create your views here.


class SearchView(View):

    template_name = "index.html"

    def get(self, request):

        context = {
        }

        return render(request, self.template_name, context)
