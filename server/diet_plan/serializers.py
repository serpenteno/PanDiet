from rest_framework import serializers
from .models import DietPlan, DietPlanMeals
from meals.serializers import MealSerializer
from tags.serializers import TagSerializer
from meals.models import Meal
from tags.models import Tag


class DietPlanMealsSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)

    # For POST request we only get id
    meal_id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all(),
        write_only=True
    )

    class Meta:
        model = DietPlanMeals
        fields = ['meal', 'meal_id', 'day_number', 'day_time']


class DietPlanSerializer(serializers.ModelSerializer):
    meals = DietPlanMealsSerializer(many=True, source='dietplanmeals_set')
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source='tags'
    )

    class Meta:
        model = DietPlan
        fields = ['id', 'name', 'description', 'tags', 'author', 'visibility', 'meals']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take meal data
        meals_data = validated_data.pop('dietplanmeals_set', [])
        diet_plan = DietPlan.objects.create(**validated_data)
        tags = validated_data.pop('tags', [])

        if tags is not None:
            diet_plan.tags.set(tags)

        # We create entries in DietPlanMeals
        for meal_item in meals_data:
            DietPlanMeals.objects.create(
                diet_plan=diet_plan,
                meal=meal_item['meal_id'],
                day_number=meal_item['day_number'],
                day_time=meal_item['day_time']
            )
        return diet_plan

    def update(self, instance, validated_data):
        meals_data = validated_data.pop('dietplanmeals_set', None)
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.set(tags)

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
                    meal=meal_item['meal_id'],
                    day_number=meal_item['day_number'],
                    day_time=meal_item['day_time']
                )

        return instance

