from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "cards"

urlpatterns = [
    path('', views.UploadFileView.as_view(), name="upload_file"),
    # caching page for 1 hour (3600 secs)
]
