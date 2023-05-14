from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from .models import Invoice


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email")
        extra_kwargs = {
            "password": {"write_only": True},
        }

        # Username was exchanged for Email in the views
        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data["username"],
                password=validated_data["password"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email=validated_data["username"],
            )
            return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ("id", "username", "email", "first_name", "last_name")
        fields = "__all__"


# User serializer
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "file_url",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        invoice = Invoice.objects.create(
            user=User.objects.get(id=user_id),
            file_url=validated_data["file_url"],
        )
        return invoice
