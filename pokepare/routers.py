from rest_framework import routers
from cards import views as card_views


router = routers.DefaultRouter()
router.register(r'cards', card_views.CardViewSet)
