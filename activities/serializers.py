from rest_framework import serializers
from .models import Category,Activity,ActivityRegistration

class CategoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class ActivityRegistrationSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField(source='account.user.username')

	class Meta:
		model = ActivityRegistration
		fields = ['id','username','is_accepted']


class DetailActivitiesSerializer(serializers.ModelSerializer):
	number_of_participants = serializers.ReadOnlyField()
	number_of_likes = serializers.ReadOnlyField()
	have_ended = serializers.ReadOnlyField()
	categories = CategoriesSerializer(many=True)
	activity_registrations = ActivityRegistrationSerializer(many=True, read_only=True)

	class Meta:
		model = Activity
		fields = '__all__'

	def create(self, validated_data):
		# Extract category data from validated_data
		categories_data = validated_data.pop('categories', [])

		# Create the activity
		activity = Activity.objects.create(**validated_data)

		# Create and associate categories with the activity
		for category_data in categories_data:
			category, created = Category.objects.get_or_create(name=category_data['name'])
			activity.categories.add(category)

		return activity

class ListActivitiesSerializer(serializers.ModelSerializer):
	number_of_likes = serializers.ReadOnlyField()
	categories = CategoriesSerializer(many=True,read_only=True)

	class Meta:
		model = Activity
		fields = ['id','number_of_likes','categories','title','photo','is_free']
