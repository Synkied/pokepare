from django.conf import settings
from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path('', views.CardView.as_view(), name="card_list"),
    path('<int:pk>', views.CardViewDetail.as_view(), name="card_detail"),
]
