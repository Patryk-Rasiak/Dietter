from rest_framework import serializers
from .models import Diet, DietDay
from meals.serializers import DietDayMealSerializer


class RetrieveDietDaySerializer(serializers.ModelSerializer):
    meals = DietDayMealSerializer(many=True)

    class Meta:
        model = DietDay
        fields = ('day', 'meals')


class CreateDietDaySerializer(serializers.ModelSerializer):
    meals = serializers.ListField(child=serializers.IntegerField(min_value=1))

    class Meta:
        model = DietDay
        fields = ('day', 'meals')


class CreateDietSerializer(serializers.ModelSerializer):
    diet_days = CreateDietDaySerializer(many=True, write_only=True)

    class Meta:
        model = Diet
        fields = ('title', 'description', 'is_public', 'diet_days')

    def create(self, validated_data):
        diet_days_data = validated_data.pop('diet_days')
        user = self.context['request'].user
        diet = Diet.objects.create(creator=user, **validated_data)

        created_days = []
        for diet_day in diet_days_data:
            meals_data = diet_day.pop('meals')
            new_diet_day = DietDay.objects.create(**diet_day)
            new_diet_day.meals.add(*meals_data)
            new_diet_day.save()
            created_days.append(new_diet_day)

        diet.diet_days.add(*created_days)
        diet.save()
        return diet


class ListDietSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    avg_calories = serializers.IntegerField()
    avg_protein = serializers.IntegerField()
    avg_carbohydrates = serializers.IntegerField()
    avg_fat = serializers.IntegerField()
    avg_rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()

    class Meta:
        model = Diet
        fields = ('id', 'creator', 'title', 'is_public', 'diet_length', 'avg_calories', 'avg_protein',
                  'avg_carbohydrates', 'avg_fat', 'avg_rating', 'ratings_count')


class RetrieveDietSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    diet_days = RetrieveDietDaySerializer(many=True)
    avg_calories = serializers.IntegerField()
    avg_protein = serializers.IntegerField()
    avg_carbohydrates = serializers.IntegerField()
    avg_fat = serializers.IntegerField()
    avg_rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()

    class Meta:
        model = Diet
        fields = ('id', 'creator', 'title', 'description', 'is_public', 'diet_length', 'diet_days',
                  'avg_calories', 'avg_protein', 'avg_carbohydrates', 'avg_fat', 'avg_rating', 'ratings_count')

