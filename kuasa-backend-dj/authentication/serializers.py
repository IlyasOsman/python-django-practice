from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'alternative_email', 'registration_no', 'phone_number', 'year_of_study')

    def create(self, validated_data):
        # Remove the confirm_password field from the validated data
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.get('password')

        # Check if password and confirm_password match
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create_user(**validated_data)
        return user