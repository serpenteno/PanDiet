from rest_framework import serializers
from .models import Meal, MealProducts
from products.models import Product


class MealProductsSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = MealProducts
        fields = ['product', 'amount']


class MealSerializer(serializers.ModelSerializer):
    products = MealProductsSerializer(many=True, source='mealproducts_set')

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'recipe', 'mass', 'author', 'visibility', 'products']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take product data
        products_data = validated_data.pop('mealproducts_set', [])
        meal = Meal.objects.create(**validated_data)

        # We create entries in MealNutrients
        for product_item in products_data:
            MealProducts.objects.create(
                meal=meal,
                product=product_item['product'],
                amount=product_item['amount']
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
                    product=product_item['product'],
                    amount=product_item['amount']
                )

        return instance

