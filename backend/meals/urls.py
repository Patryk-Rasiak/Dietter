from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import MealViewSet

router = SimpleRouter()
router.register(r'', MealViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
