from rest_framework import serializers
from .models import DietPlan, DietPlanMeals
from diet_plan.models import DietPlan


class DietPlanMealsSerializer(serializers.ModelSerializer):
    diet_plan = serializers.PrimaryKeyRelatedField(queryset=DietPlan.objects.all())

    class Meta:
        model = DietPlanMeals
        fields = ['diet_plan']


class DietPlanSerializer(serializers.ModelSerializer):
    diet_plans = DietPlanMealsSerializer(many=True, source='diet_planmeals_set')

    class Meta:
        model = DietPlan
        fields = ['id', 'name', 'description', 'tags', 'author', 'visibility', 'meals']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take meal data
        meals_data = validated_data.pop('diet_planmeals_set', [])
        diet_plan = DietPlan.objects.create(**validated_data)

        # We create entries in DietPlanMeals
        for meal_item in meals_data:
            DietPlanMeals.objects.create(
                diet_plan=diet_plan,
                meal=meal_item['meal']
            )
        return diet_plan

    def update(self, instance, validated_data):
        meals_data = validated_data.pop('diet_planmeals_set', None)

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
                    meal=meal_item['meal']
                )

        return instance

