from django.views import View
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter

from .serializers import SetSerializer
from .models import Set

# Create your views here.


class SetFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut
    # but it won't let you use "exclude"
    class Meta:
        model = Set
        exclude = ['image']


class SetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sets to be viewed or edited.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = SetFilter
    ordering_fields = '__all__'  # what field can be ordered via the API
    ordering = ['release_date']  # default ordering


class SetView(View):

    template_name = "index.html"

    def get(self, request):

        sets = Set.objects.all()

        context = {
            "sets": sets,
        }

        return render(request, self.template_name, context)


class SetViewDetail(View):

    template_name = "index.html"

    def get(self, request, code):

        context = {
        }

        return render(request, self.template_name, context)
