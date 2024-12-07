from django.db import models


class Nutrient(models.Model):
    UNIT_CHOICES = [
        ('g', 'Gram'),
        ('mg', 'Milligram'),
        ('mcg', 'Microgram'),
        ('kg', 'Kilogram'),
        ('ml', 'Milliliter'),
        ('l', 'Liter'),
    ]

    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.unit})"
