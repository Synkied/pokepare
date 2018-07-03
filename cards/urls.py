from django.conf import settings
from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path('', views.CardView.as_view(), name="card_list"),
    path('<str:name>', views.CardViewDetail.as_view(), name="card_detail"),
]
