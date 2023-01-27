from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .viewsets import DietViewSet

router = SimpleRouter()
router.register(r'', DietViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
