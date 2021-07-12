from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from uploads.views import UploadFileView

from .routers import router
from .views import SearchView

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    # path('cards/', include('cards.urls'), name="cards"),
    # path('pokemons/', include('pokemons.urls'), name="pokemons"),
    # path('cardsets/', include('cardsets.urls'), name="cardsets"),
    path('search/', SearchView.as_view(), name="search"),
    path(
        'file-upload/',
        csrf_exempt(UploadFileView.as_view()),
        name="file_upload"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
