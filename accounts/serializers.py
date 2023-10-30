from .models import CustomUser, Account, JoinClubForm
from rest_framework import serializers
from django.db import IntegrityError


class CustomUserSerializer(serializers.ModelSerializer):
    last_login = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        exclude = [
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            gender=validated_data["gender"],
            phone_number=validated_data["phone_number"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        Account.objects.create(user=user)
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    photo_url = serializers.ReadOnlyField(source="get_photo_url")

    class Meta:
        model = Account
        fields = "__all__"
        kwargs = {"photo": {"write_only": True}}


class ListAccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    photo_url = serializers.ReadOnlyField(source="get_photo_url")

    class Meta:
        model = Account
        fields = "__all__"
        extra_kwargs = {
                    "photo": {"write_only": True},
                }

class MainAccountSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=False)
    photo_url = serializers.ReadOnlyField(source="get_photo_url")

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = (
            "role",
            "date_joined",
            "last_login",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "photo": {"write_only": True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create(**user_data)

        account = Account.objects.create(user=user, **validated_data)
        return account

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")

        user = instance.user

        for attr, value in user_data.items():
            if attr == "password":
                user.set_password(value)
            else:
                setattr(user, attr, value)

        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SimpleAccountSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Account
        fields = ["id", "username", "photo"]


class JoinClubFormSerializer(serializers.ModelSerializer):
    account = SimpleAccountSerializer(many=False, read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = JoinClubForm
        fields = "__all__"

    def create(self, validated_data):
        account = self.context["request"].user.account
        validated_data["account"] = account  # Ensure the account is set

        try:
            instance = JoinClubForm.objects.create(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(
                "You have already submitted a join club form."
            )

        return instance
