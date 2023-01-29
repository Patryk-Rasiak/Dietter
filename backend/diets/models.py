from django.db import models
from django.contrib.auth.models import User
from meals.models import Meal


class DietDay(models.Model):
    day = models.PositiveIntegerField()
    meals = models.ManyToManyField(Meal, related_name='diet_days', blank=True)


class Diet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diets',
                                default=None, null=True, blank=True)
    title = models.CharField(max_length=40)
    diet_length = models.PositiveIntegerField(default=1)
    description = models.TextField(default='')
    is_public = models.BooleanField(default=False)
    diet_days = models.ManyToManyField(DietDay, blank=True)

    class Meta:
        unique_together = ('title', 'creator')
