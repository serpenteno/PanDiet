from rest_framework import serializers
from .models import Product, ProductNutrient
from nutrients.models import Nutrient


class ProductNutrientSerializer(serializers.ModelSerializer):
    nutrient = serializers.PrimaryKeyRelatedField(queryset=Nutrient.objects.all())

    class Meta:
        model = ProductNutrient
        fields = ['nutrient', 'amount']


class ProductSerializer(serializers.ModelSerializer):
    nutrients = ProductNutrientSerializer(many=True, source='productnutrient_set')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'mass', 'author', 'visibility', 'nutrients']
        read_only_fields = ['id', 'author']

    def create(self, validated_data):
        # We take nutrient data
        nutrients_data = validated_data.pop('productnutrient_set', [])
        product = Product.objects.create(**validated_data)

        # We create entries in ProductNutrient
        for nutrient_item in nutrients_data:
            ProductNutrient.objects.create(
                product=product,
                nutrient=nutrient_item['nutrient'],
                amount=nutrient_item['amount']
            )
        return product

    def update(self, instance, validated_data):
        nutrients_data = validated_data.pop('productnutrient_set', None)

        # Update product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nutrient data for product in ProductNutrient
        if nutrients_data is not None:
            instance.productnutrient_set.all().delete()
            for nutrient_item in nutrients_data:
                ProductNutrient.objects.create(
                    product=instance,
                    nutrient=nutrient_item['nutrient'],
                    amount=nutrient_item['amount']
                )

        return instance

