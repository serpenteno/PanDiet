from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import DietPlan
from meals.models import Meal


@receiver(m2m_changed, sender=Meal.tags.through)
def update_dietplan_tags_on_meal_tags_change(sender, instance, action, **kwargs):
    """
    Update tags of a diet plan when tags of one of its products change
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        # All diet plans related to edited meal
        related_dietplans = DietPlan.objects.filter(meals=instance)

        # For each related diet plan update tags
        for diet_plan in related_dietplans:
            diet_plan.update_dietplan_tags()
            diet_plan.save()  # Save object
