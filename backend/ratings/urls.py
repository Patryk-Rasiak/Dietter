from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import RatingViewSet

router = SimpleRouter()
router.register(r'', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
