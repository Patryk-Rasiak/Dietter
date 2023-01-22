from rest_framework import serializers

from .models import Meal, Ingredient, NutritionalValues
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit')


class NutritionalValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionalValues
        fields = ('calories', 'protein', 'carbohydrates', 'fat')


class MealSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=True)
    nutritional_values = NutritionalValuesSerializer(required=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'photo', 'recipe', 'is_public', 'ingredients', 'nutritional_values')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        nutritional_values_data = validated_data.pop('nutritional_values')
        user = self.context['request'].user
        meal = Meal.objects.create(author=user, **validated_data)
        meal.save()

        for ingredient in ingredients_data:
            Ingredient.objects.create(meal=meal, **ingredient)
        NutritionalValues.objects.create(meal=meal, **nutritional_values_data)

        return meal

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = instance.author.username
        return data

