from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile, Preferences, RoomListing
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

# 1. User & Student Profile Serializers
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'university',
            'registration_number',
            'phone_number',
            'is_verified'
        ]
        read_only_fields = [ 'university', 
                            'registration_number', 
                            'is_verified' 
                            ]

class UserSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile'
        ]
        read_only_fields = ['username', 'email']

    def update(self, instance, validated_data):
        # Get profile data if it was included in the request
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.save()

        # Update StudentProfile fields
        if profile_data:
            profile = instance.profile

            for field, value in profile_data.items():
                setattr(profile, field, value)

            profile.save()

        return instance

# 2. Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    university = serializers.CharField(write_only=True)
    registration_number = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'university',
            'registration_number',
            'phone_number'
        ]

    def validate_email(self, value):
        value = value.lower().strip()

        if not value.endswith('@students.ku.ac.ke'):
            raise serializers.ValidationError(
                'Please use your Kenyatta University student email.'
            )

        return value

    def create(self, validated_data):
        university = validated_data.pop('university')
        reg_num = validated_data.pop('registration_number')
        phone = validated_data.pop('phone_number')

        # Create the user
        user = User.objects.create_user(**validated_data)

        # Generate a 6-digit verification code
        verification_code = str(random.randint(100000, 999999))

        # Create student profile
        StudentProfile.objects.create(
            user=user,
            university=university,
            registration_number=reg_num,
            phone_number=phone,
            verification_code=verification_code,
            verification_code_created_at=timezone.now()
        )

        # Send verification email
        send_mail(
            subject='Verify your Kejani account',
            message=f'''
Hello {user.first_name or user.username},

Welcome to Kejani!

Your university email verification code is:

{verification_code}

Enter this code in Kejani to verify your account.

If you did not create this account, please ignore this email.
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
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