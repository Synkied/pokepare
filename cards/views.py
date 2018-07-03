from django.views import View
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CardSerializer
from .models import Card

# Create your views here.


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = '__all__'


class CardView(View):

    template_name = "cards.html"

    def get(self, request):

        cards = Card.objects.all()

        context = {
            "cards": cards,
        }

        return render(request, self.template_name, context)


class CardViewDetail(View):

    template_name = "cards.html"

    def get(self, request, name):

        context = {
        }

        return render(request, self.template_name, context)
