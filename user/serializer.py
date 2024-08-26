from rest_framework import serializers
from user.models import (
    User
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["is_superuser", "is_staff", "user_reg_status", "password"]
        depth = 1

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    user_phone = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True)
    notery_reg_number = serializers.CharField(required=True)
    estamp_number = serializers.CharField(required=True)
    office_address = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = "__all__"