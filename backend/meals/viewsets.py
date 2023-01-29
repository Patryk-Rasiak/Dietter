from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Meal
from .serializers import CreateMealSerializer, ListMealSerializer, RetrieveMealSerializer
from ratings.serializers import RatingSerializer
from django.db.models import Q, Avg, Count
from django.db.models.functions import Round


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.select_related("author", "nutritional_values")
    serializer_class = ListMealSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create':
            return CreateMealSerializer(*args, **kwargs)
        elif self.action == 'retrieve':
            return RetrieveMealSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.annotate(
            avg_rating=Round(Avg('ratings__value'), 1),
            ratings_count=Count('ratings', distinct=True)
        )
        if self.action in ('list', 'retrieve'):
            return queryset.filter(Q(is_public=True) | Q(author=self.request.user))
        elif self.action == 'user_meals':
            return queryset.filter(author=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        meal = self.get_object()
        meal_data = self.get_serializer(meal).data

        rating = meal.ratings.filter(author=request.user).first()
        if rating:
            rating_serializer = RatingSerializer(rating)
            meal_data['user_rating'] = rating_serializer.data

        return Response(meal_data)

    @action(detail=False, methods=['get'])
    def user_meals(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
