from rest_framework import serializers
from .models import CustomUser,Account

class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id','username', 'email', 'first_name', 'last_name', 'gender', 'phone_number','password']
		extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

	def create(self, validated_data):
		user = CustomUser.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			gender=validated_data['gender'],
			phone_number=validated_data['phone_number'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
		)
		user.set_password(validated_data['password'])
		Account.objects.create(user=user)
		user.save()
		return user
	
class AccountSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField(source='user.username')

	class Meta:
		model = Account
		fields = '__all__'

class SimpleAccountSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField(source='user.username')

	class Meta:
		model = Account
		fields = ['id','username','photo']
