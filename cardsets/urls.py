from django.urls import path

from . import views

app_name = "cardsets"

urlpatterns = [
    path('', views.CardSetView.as_view(), name="cardset_list"),
    path(
        '<str:code>',
        views.CardSetViewDetail.as_view(),
        name="cardset_detail"
    ),
]
