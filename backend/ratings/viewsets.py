from rest_framework.viewsets import ModelViewSet
from .models import Rating
from rest_framework.permissions import IsAuthenticated
from .serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer







