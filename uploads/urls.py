from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "cards"

urlpatterns = [
    path('', csrf_exempt(views.UploadFileView.as_view()), name="upload_file"),
    # caching page for 1 hour (3600 secs)
]
