from django.urls import path

from . import views

app_name = "sets"

urlpatterns = [
    path('', views.CardSetView.as_view(), name="set_list"),
    path('<str:code>', views.CardSetViewDetail.as_view(), name="set_detail"),
]
