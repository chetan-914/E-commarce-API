from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'name', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number = validated_data['phone_number'],
            name = validated_data['name'],
            password = validated_data['password'],
            email = validated_data.get('email')
        )
        return user
    