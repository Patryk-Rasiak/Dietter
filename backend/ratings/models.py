from django.db import models
from django.contrib.auth.models import User
from meals.models import Meal
from diets.models import Diet


class Rating(models.Model):
    RATING_CHOICES = [(x/2, x/2) for x in range(0, 11)]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(choices=RATING_CHOICES)
    description = models.TextField(blank=True, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
