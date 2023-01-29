from django_filters import rest_framework as filters
from .models import Diet


class DietFilterSet(filters.FilterSet):
    avg_calories = filters.RangeFilter()
    avg_protein = filters.RangeFilter()
    avg_carbohydrates = filters.RangeFilter()
    avg_fat = filters.RangeFilter()
    avg_rating = filters.RangeFilter()
    ratings_count = filters.RangeFilter()

    class Meta:
        model = Diet
        fields = ['avg_calories', 'avg_protein', 'avg_carbohydrates', 'avg_fat', 'avg_rating', 'ratings_count']
