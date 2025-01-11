from rest_framework import serializers
from .models import DietPlan, DietPlanMeals
from meals.serializers import MealSerializer
from tags.serializers import TagSerializer


class DietPlanMealsSerializer(serializers.ModelSerializer):
    meal = MealSerializer()

    class Meta:
        model = DietPlanMeals
        fields = ['meal', 'day_number', 'day_time']


class DietPlanSerializer(serializers.ModelSerializer):
    meals = DietPlanMealsSerializer(many=True, source='dietplanmeals_set')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = DietPlan
        fields = ['id', 'name', 'description', 'tags', 'author', 'visibility', 'meals']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take meal data
        meals_data = validated_data.pop('dietplanmeals_set', [])
        diet_plan = DietPlan.objects.create(**validated_data)

        # We create entries in DietPlanMeals
        for meal_item in meals_data:
            DietPlanMeals.objects.create(
                diet_plan=diet_plan,
                meal=meal_item['meal'],
                day_number=meal_item['day_number'],
                day_time=meal_item['day_time']
            )
        return diet_plan

    def update(self, instance, validated_data):
        meals_data = validated_data.pop('dietplanmeals_set', None)

        # Update diet plan
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update meal data for diet plan in DietPlanMeals
        if meals_data is not None:
            instance.diet_planmeals_set.all().delete()
            for meal_item in meals_data:
                DietPlanMeals.objects.create(
                    diet_plan=instance,
                    meal=meal_item['meal'],
                    day_number=meal_item['day_number'],
                    day_time=meal_item['day_time']
                )

        return instance

