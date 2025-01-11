from django.db import models
from nutrients.models import Nutrient
from users.models import User
from tags.models import Tag


class Product(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    mass = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)

    nutrients = models.ManyToManyField(Nutrient, through='ProductNutrient')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author} ({self.visibility})"


class ProductNutrient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.nutrient.name}: {self.amount} {self.nutrient.unit}"
