from django.urls import path
from django.views.decorators.cache import cache_page

from .views import CardViewDetail
from .views import CardViewList

app_name = "cards"

urlpatterns = [
    path('', cache_page(60 * 60)(CardViewList.as_view()), name="card_list"),
    path('<str:unique_id>', cache_page(60 * 60)(
        CardViewDetail.as_view()
    ), name="card_detail"),
]
