from django.db import models
from django.contrib.auth.models import User


class NutritionalValues(models.Model):
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
    name = models.CharField(max_length=25)
    amount = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)


class Meal(models.Model):
    TYPE_CHOICES = [
        ('breakfast', 'breakfast'),
        ('second_breakfast', 'second_breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('snacks', 'snacks')
    ]
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='meals', default=None, null=True,
                               blank=True)
    name = models.CharField(max_length=40)
    meal_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    recipe = models.TextField()
    is_public = models.BooleanField(default=False)
    nutritional_values = models.OneToOneField(NutritionalValues, on_delete=models.CASCADE, related_name='meal')
    ingredients = models.ManyToManyField(Ingredient, related_name='meal')

    class Meta:
        unique_together = ('name', 'author')




