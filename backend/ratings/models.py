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

    def _update_rating_stats(self):
        rated_item = self.meal if self.meal else self.diet
        rated_item.average_rating = rated_item.ratings.all().aggregate(models.Avg('value'))['value__avg']
        rated_item.ratings_count = rated_item.ratings.count()
        rated_item.save()

    def save(self, *args, **kwargs):
        self._update_rating_stats()
        super().save(*args, **kwargs)
