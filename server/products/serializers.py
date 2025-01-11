from rest_framework import serializers
from .models import Product, ProductNutrient
from nutrients.models import Nutrient
from tags.serializers import TagSerializer
from nutrients.serializers import NutrientSerializer
from tags.models import Tag


class ProductNutrientSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer(read_only=True)

    # For POST request we only get id
    nutrient_id = serializers.PrimaryKeyRelatedField(
        queryset=Nutrient.objects.all(),
        write_only=True
    )

    class Meta:
        model = ProductNutrient
        fields = ['nutrient_id', 'nutrient', 'amount']


class ProductSerializer(serializers.ModelSerializer):
    nutrients = ProductNutrientSerializer(many=True, source='productnutrient_set')
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source='tags'
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'mass', 'tags', 'author', 'visibility', 'nutrients', 'tags_ids']
        read_only_fields = ['id', 'author', 'tags']

    def create(self, validated_data):
        # We take nutrient data
        nutrients_data = validated_data.pop('productnutrient_set', [])
        tags = validated_data.pop('tags', [])
        product = Product.objects.create(**validated_data)

        if tags is not None:
            product.tags.set(tags)

        # We create entries in ProductNutrient
        for nutrient_item in nutrients_data:
            ProductNutrient.objects.create(
                product=product,
                nutrient=nutrient_item['nutrient_id'],
                amount=nutrient_item['amount']
            )

        return product

    def update(self, instance, validated_data):
        nutrients_data = validated_data.pop('productnutrient_set', None)
        tags = validated_data.pop('tags', None)

        # Update product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        # Update nutrient data for product in ProductNutrient
        if nutrients_data is not None:
            instance.productnutrient_set.all().delete()
            for nutrient_item in nutrients_data:
                ProductNutrient.objects.create(
                    product=instance,
                    nutrient=nutrient_item['nutrient_id'],
                    amount=nutrient_item['amount']
                )

        return instance
