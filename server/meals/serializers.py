from rest_framework import serializers
from .models import Meal, MealProducts
from products.serializers import ProductSerializer
from tags.serializers import TagSerializer
from products.models import Product
from tags.models import Tag


class MealProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    # For POST request we only get id
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = MealProducts
        fields = ['product', 'product_id', 'amount']


class MealSerializer(serializers.ModelSerializer):
    products = MealProductsSerializer(many=True, source='mealproducts_set')
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source='tags'
    )

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'recipe', 'mass', 'tags', 'author', 'visibility', 'products', 'tags_ids']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take product data
        products_data = validated_data.pop('mealproducts_set', [])
        meal = Meal.objects.create(**validated_data)
        tags = validated_data.pop('tags', [])

        if tags is not None:
            meal.tags.set(tags)

        # We create entries in MealNutrients
        for product_item in products_data:
            MealProducts.objects.create(
                meal=meal,
                product=product_item['product_id'],
                amount=product_item['amount']
            )
        return meal

    def update(self, instance, validated_data):
        products_data = validated_data.pop('mealproducts_set', None)
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.set(tags)

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
                    product=product_item['product_id'],
                    amount=product_item['amount']
                )

        return instance

