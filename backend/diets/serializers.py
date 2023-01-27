from rest_framework import serializers
from .models import Diet, DietDay


class DietDaySerializer(serializers.ModelSerializer):
    meals = serializers.ListField(child=serializers.IntegerField(min_value=1))

    class Meta:
        model = DietDay
        fields = ('day', 'meals')


class CreateDietSerializer(serializers.ModelSerializer):
    diet_days = DietDaySerializer(many=True, write_only=True)

    class Meta:
        model = Diet
        fields = ('title', 'description', 'is_public', 'diet_days')

    def create(self, validated_data):
        diet_days_data = validated_data.pop('diet_days')
        user = self.context['request'].user
        diet = Diet.objects.create(creator=user, **validated_data)
        diet.save()

        created_days = []
        for diet_day in diet_days_data:
            meals_data = diet_day.pop('meals')
            new_diet_day = DietDay.objects.create(**diet_day)
            new_diet_day.meals.add(*meals_data)
            created_days.append(new_diet_day)

        diet.diet_days.add(*created_days)

        return diet


class DietSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diet
        fields = ('id', 'creator', 'title', 'description', 'is_public')
