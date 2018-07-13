from django.conf import settings
from django.urls import path

from . import views

app_name = "sets"

urlpatterns = [
    path('', views.SetView.as_view(), name="set_list"),
    path('<str:code>', views.SetViewDetail.as_view(), name="set_detail"),
]
