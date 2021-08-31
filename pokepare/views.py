import hashlib

from cards.models import Card

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


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


class EbayNotificationView(View):

    def get(self, request):
        challenge_code = request.GET.get('challenge_code')
        compute = '%s%s%s' % (
            challenge_code,
            'pokepare_verification_token_42ql',
            request.build_absolute_uri(
                reverse('ebay_marketplace_notification')
            )
        )
        compute = compute.encode('utf-8')
        verif = hashlib.sha256(compute)
        verif = verif.hexdigest()

        return JsonResponse({'challengeResponse': verif})

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return HttpResponse(status=200)
