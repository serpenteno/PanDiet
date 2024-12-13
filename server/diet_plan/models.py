from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
from meals.models import Meal


class DietPlan(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"), 
        ("private", "Private")
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)

    meals = models.ManyToManyField(Meal, through='DietPlanMeals')

    def clean(self):
        if self.visibility not in dict(self.VISIBILITY_CHOICES):
            raise ValidationError("Invalid visibility")


class DietPlanMeals(models.Model):
    DAY_NUMBER = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    ]

    DAY_TIME = [
        ('breakfast', 'Breakfast'),
        ('a.m. snack', 'A.M. Snack'),
        ('lunch', 'Lunch'),
        ('p.m. snack', 'P.M. Snack'),
        ('dinner', 'Dinner')
    ]

    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day_number = models.CharField(max_length=10, choices=DAY_NUMBER)
    day_time = models.CharField(max_length=10, choices=DAY_TIME)
    
    def __str__(self):
        return f"{self.diet_plan.name} - {self.meal.name}"