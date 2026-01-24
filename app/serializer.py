from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class product_detailsserializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(use_url=True)
#     product_category = serializers.SlugRelatedField(
#     queryset=products_category.objects.all(),
#     slug_field="category"
# )

    class Meta:
        model = product_details
        fields = '__all__'


class loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User

    # @classmethod
    # def  get_token(cls,user):
    #     token=super().get_token(user)
    #     return token
    
    def validate(self, validated_data):

        username = validated_data.get("username")
        password = validated_data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        validated_data["user"] = user
        return validated_data   # ✅ MUST return dict

class signupserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],# REQUIRED
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""), # OPTIONAL so we use here get
            last_name=validated_data.get("last_name", ""),
        )
        return user