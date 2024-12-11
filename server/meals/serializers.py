from rest_framework import serializers
from .models import Meal, MealProducts
from meals.models import Meal


class MealProductsSerializer(serializers.ModelSerializer):
    meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all())

    class Meta:
        model = MealProducts
        fields = ['meal']


class MealSerializer(serializers.ModelSerializer):
    products = MealProductsSerializer(many=True, source='mealproducts_set')

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'recipe', 'mass', 'tags', 'author', 'visibility', 'products']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take product data
        products_data = validated_data.pop('mealnutrients_set', [])
        meal = Meal.objects.create(**validated_data)

        # We create entries in MealNutrients
        for product_item in products_data:
            MealProducts.objects.create(
                meal=meal,
                product=product_item['product']
            )
        return meal

    def update(self, instance, validated_data):
        products_data = validated_data.pop('mealproducts_set', None)

        # Update meal
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update product data for meal in MealProducts
        if products_data is not None:
            instance.mealproducts_set.all().delete()
            for product_item in products_data:
                MealProducts.objects.create(
                    meal=instance,
                    product=product_item['nutrient']
                )

        return instance

