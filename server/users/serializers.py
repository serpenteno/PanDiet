from rest_framework import serializers
from .models import User, DietitianClient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'diet_plan', 'is_active']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class DietitianClientSerializer(serializers.ModelSerializer):
    dietitian = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='dietitian'))
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='client'))

    class Meta:
        model = DietitianClient
        fields = ['id', 'dietitian', 'client']
        read_only_fields = ['id']
