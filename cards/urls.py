from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "cards"

urlpatterns = [
    path('', cache_page(60 * 60)(views.CardView.as_view()), name="card_list"),
    path('<str:unique_id>', cache_page(60 * 60)(
        views.CardViewDetail.as_view()
    ), name="card_detail"),
    # caching page for 1 hour (3600 secs)
]
