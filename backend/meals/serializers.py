from rest_framework import serializers

from .models import Meal, Ingredient, NutritionalValues


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit')


class NutritionalValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionalValues
        fields = ('calories', 'protein', 'carbohydrates', 'fat')


class CreateMealSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=True, write_only=True)
    nutritional_values = NutritionalValuesSerializer(required=True, write_only=True)
    photo = serializers.ImageField(write_only=True, allow_null=True)
    is_public = serializers.BooleanField(write_only=True)
    recipe = serializers.CharField(write_only=True)
    meal_type = serializers.CharField(write_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'photo', 'recipe', 'is_public', 'meal_type', 'ingredients', 'nutritional_values')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        nutritional_values_data = validated_data.pop('nutritional_values')
        nutritional_values = NutritionalValues.objects.create(**nutritional_values_data)
        user = self.context['request'].user
        meal = Meal.objects.create(author=user, nutritional_values=nutritional_values, **validated_data)

        ingredients = []
        for ingredient in ingredients_data:
            ingredients.append(Ingredient.objects.create(**ingredient))

        meal.ingredients.add(*ingredients)

        meal.save()
        return meal


class ListMealSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    nutritional_values = NutritionalValuesSerializer()
    avg_rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()

    class Meta:
        model = Meal
        fields = ('id', 'author', 'name', 'meal_type', 'nutritional_values', 'avg_rating', 'ratings_count')


class RetrieveMealSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    ingredients = IngredientSerializer(many=True)
    nutritional_values = NutritionalValuesSerializer()
    avg_rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()

    class Meta:
        model = Meal
        fields = ('id', 'author', 'name', 'photo', 'recipe', 'is_public', 'ingredients', 'nutritional_values',
                  'avg_rating', 'ratings_count')
