from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ListDietSerializer, CreateDietSerializer, RetrieveDietSerializer
from .models import Diet
from .filters import DietFilterSet
from django.db import transaction
from django.db.models import Avg, Count, IntegerField
from django.db.models.functions import Cast, Round


class DietViewSet(ModelViewSet):
    serializer_class = ListDietSerializer
    queryset = Diet.objects.select_related("creator")
    filterset_class = DietFilterSet
    ordering_fields = [
                       'avg_calories',
                       'avg_protein',
                       'avg_carbohydrates',
                       'avg_fat',
                       'avg_rating',
                       'ratings_count',
                       ]
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create':
            return CreateDietSerializer(*args, **kwargs)
        elif self.action == 'retrieve':
            return RetrieveDietSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.annotate(
            avg_rating=Round(Avg('ratings__value'), 1),
            ratings_count=Count('ratings', distinct=True),
            avg_calories=Cast(Avg('diet_days__meals__nutritional_values__calories'), IntegerField()),
            avg_protein=Cast(Avg('diet_days__meals__nutritional_values__protein'), IntegerField()),
            avg_carbohydrates=Cast(Avg('diet_days__meals__nutritional_values__carbohydrates'), IntegerField()),
            avg_fat=Cast(Avg('diet_days__meals__nutritional_values__fat'), IntegerField())
        )

        if self.action == 'list':
            return queryset.filter(is_public=True)
        elif self.action == 'user_diets':
            return queryset.filter(creator=self.request.user)

        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'Diet': 'Diet successfully created'}
        return response

    @action(detail=False, methods=['get'])
    def user_diets(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

