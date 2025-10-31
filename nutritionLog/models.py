from django.db import models
from django.conf import settings
from django.utils import timezone


class NutritionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nutrition_logs')
    date = models.DateField(default=timezone.localdate)

    calories_current = models.IntegerField(default=0)
    calories_goal    = models.IntegerField(default=2000)

    carbs_current    = models.IntegerField(default=0)
    carbs_goal       = models.IntegerField(default=100)

    protein_current  = models.IntegerField(default=0)
    protein_goal     = models.IntegerField(default=130)

    fiber_current    = models.IntegerField(default=0)
    fiber_goal       = models.IntegerField(default=55)

    fat_current      = models.IntegerField(default=0)
    fat_goal         = models.IntegerField(default=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='uniq_user_date_nutrition_log')
        ]

    def __str__(self):
        return f'{self.user.email} • {self.date}'


class Recipe(models.Model):
    MEAL_CHOICES = (
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('SNACK', 'Snack'),
    )

    title       = models.CharField(max_length=255)
    subtitle    = models.CharField(max_length=255, blank=True)
    meal_type   = models.CharField(max_length=20, choices=MEAL_CHOICES, default='BREAKFAST')
    ingredients = models.JSONField(default=list)
    steps       = models.JSONField(default=list)

    def __str__(self):
        return self.title