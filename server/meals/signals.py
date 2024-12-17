from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Meal
from products.models import Product


@receiver(m2m_changed, sender=Product.tags.through)
def update_meal_tags_on_product_tags_change(sender, instance, action, **kwargs):
    """
    Update tags of meal when tags of one of uts product changes
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        # All meals related to edited product
        related_meals = Meal.objects.filter(products=instance)

        # For each related meal update tags
        for meal in related_meals:
            meal.update_meal_tags()
            meal.save()  # Save object
