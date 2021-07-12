from django.urls import path

from .views import CardSetDetailView
from .views import CardSetListView

app_name = "cardsets"

urlpatterns = [
    path('', CardSetListView.as_view(), name="cardset_list"),
    path(
        '<str:code>',
        CardSetDetailView.as_view(),
        name="cardset_detail"
    ),
]
