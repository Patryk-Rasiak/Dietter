from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Meal
from .serializers import CreateMealSerializer, ListMealSerializer


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.select_related("author", "nutritional_values")
    serializer_class = ListMealSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create':
            return CreateMealSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(is_public=True)
        elif self.action == 'user_meals':
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    @action(detail=False, methods=['get'])
    def user_meals(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
