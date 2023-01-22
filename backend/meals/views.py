from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Meal
from .serializers import MealSerializer


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_meals(self, request):
        meals = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)
