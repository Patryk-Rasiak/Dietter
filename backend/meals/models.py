from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals', default=None, null=True, blank=True)
    name = models.CharField(max_length=40)
    photo = models.ImageField(upload_to='photos/', blank=True)
    recipe = models.TextField()
    is_public = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'author')


class NutritionalValues(models.Model):
    meal = models.OneToOneField(Meal, on_delete=models.CASCADE, related_name='nutritional_values')
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()


class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        ('piece', 'piece'),
        ('pint', 'pint'),
        ('fl oz', 'fl oz'),
        ('tbsp', 'tbsp'),
        ('tsp', 'tsp'),
    ]
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=25)
    amount = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

