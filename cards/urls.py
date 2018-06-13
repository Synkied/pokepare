from django.conf import settings
from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path('', views.CardsView.as_view(), name="cards")
]
