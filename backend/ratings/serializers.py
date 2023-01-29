from django.db.models import Q
from rest_framework import serializers
from .models import Rating
from rest_framework.exceptions import ValidationError


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'value', 'description', 'meal', 'diet')

    def create(self, validated_data):
        meal = validated_data.get('meal')
        diet = validated_data.get('diet')
        user = self.context['request'].user

        # Preventing both being null or both having value
        if (meal and diet) or not (meal or diet):
            raise ValidationError("Meal or Diet must be set")

        # Preventing from rating your own meal/diet
        if meal and meal.author == user:
            raise ValidationError("Cannot rate your own meal!")
        if diet and diet.creator == user:
            raise ValidationError("Cannot rate your own diet!")

        # Checking if user has not already rated this meal/diet
        if Rating.objects.filter(Q(author=user) & Q(Q(meal=meal) | Q(diet=diet))).exists():
            raise ValidationError("This user already rated it")

        rating = Rating.objects.create(author=user, **validated_data)
        rating.save()

        return rating

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user != instance.author:
            raise ValidationError("Cannot update someone else's meal!")

        return super().update(instance, validated_data)
