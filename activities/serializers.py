from rest_framework import serializers
from .models import Category, Activity, ActivityRegistration
from accounts.serializers import SimpleAccountSerializer


# Categories Serializers
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data["name"]
        categorie = Category.objects.filter(name=name).first()

        if categorie:
            return categorie
        else:
            return super().create(validated_data)


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


# Activities Serializers
class UpdateActivitiesSerializer(serializers.ModelSerializer):
    categories = SimpleCategorySerializer(many=True)

    class Meta:
        model = Activity
        fields = [
            "categories",
            "title",
            "photo",
            "is_free",
            "price",
            "description",
            "location",
            "max_participants",
            "date",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr != "categories":
                setattr(instance, attr, value)

        if "categories" in validated_data:
            updated_categories = []
            for category_data in validated_data["categories"]:
                category, created = Category.objects.get_or_create(
                    name=category_data["name"]
                )
                updated_categories.append(category)
            instance.categories.set(updated_categories)

        instance.save()
        return instance


class DetailActivitiesSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.ReadOnlyField()
    posted_by = SimpleAccountSerializer(many=False)
    categories = SimpleCategorySerializer(many=True)
    likes = SimpleAccountSerializer(many=True)
    registred_accounts = SimpleAccountSerializer(many=True, read_only=True)
    photo_url = serializers.ReadOnlyField(source="get_photo_url")

    class Meta:
        model = Activity
        exclude = ["photo"]


class ListActivitiesSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.ReadOnlyField()
    categories = SimpleCategorySerializer(many=True, read_only=True)
    photo_url = serializers.ReadOnlyField(source="get_photo_url")

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "photo_url",
            "is_free",
            "number_of_likes",
            "categories",
            "created_at",
        ]


class CreateActivitiesSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True, required=False)

    class Meta:
        model = Activity
        exclude = ["posted_by"]

    def create(self, validated_data):
        posted_by = self.context["request"].user.account
        categories_data = validated_data.pop("categories", [])

        activity = Activity.objects.create(**validated_data, posted_by=posted_by)

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data["name"]
            )
            activity.categories.add(category)

        return activity


# ActivityRegistration Serializers
class AdminActivityRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="account.user.username")

    class Meta:
        model = ActivityRegistration
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class NonAdminActivityRegistrationSerializer(serializers.ModelSerializer):
    activity = ListActivitiesSerializer

    class Meta:
        model = ActivityRegistration
        exclude = ["account"]
        read_only_fields = ("is_payed", "status", "created_at", "updated_at")

    def create(self, validated_data):
        # Get the user's account from the request
        account = self.context["request"].user.account

        # Try to get an existing ActivityRegistration or create a new one if it doesn't exist
        activity_registration, created = ActivityRegistration.objects.get_or_create(
            account=account, activity=validated_data["activity"]
        )

        return activity_registration
