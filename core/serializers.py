from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile, Preferences, RoomListing

# 1. User & Student Profile Serializers
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['university', 'registration_number', 'phone_number', 'is_verified']

class UserSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

# 2. Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    university = serializers.CharField(write_only=True)
    registration_number = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'university', 'registration_number', 'phone_number']

    def create(self, validated_data):
        university = validated_data.pop('university')
        reg_num = validated_data.pop('registration_number')
        phone = validated_data.pop('phone_number')

        user = User.objects.create_user(**validated_data)

        StudentProfile.objects.create(
            user=user,
            university=university,
            registration_number=reg_num,
            phone_number=phone
        )
        return user

# 3. Preferences Serializer
class PreferencesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Preferences
        fields = ['id', 'user', 'budget_max', 'preferred_location', 'cleanliness_level', 'study_habits', 'smoking_allowed', 'guests_allowed']

# 4. Room Listing Serializer
class RoomListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RoomListing
        fields = ['id', 'owner', 'title', 'description', 'location', 'total_rent', 'rent_per_person', 'rooms_available', 'is_active', 'created_at']