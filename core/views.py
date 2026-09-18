from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from .models import StudentProfile, Preferences, RoomListing
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    PreferencesSerializer, 
    RoomListingSerializer
)

# 1. User Registration Endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# 2. User Login Endpoint (Generates Auth Token)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check whether the student's email has been verified
            if not user.profile.is_verified:
                return Response(
                    {
                        'error': 'Please verify your university email before logging in.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid Credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response(
                {'error': 'Email and verification code are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email.lower().strip())
            profile = user.profile
        except User.DoesNotExist:
            return Response(
                {'error': 'No account found with this email.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if profile.is_verified:
            return Response(
                {'message': 'Email is already verified.'},
                status=status.HTTP_200_OK
            )

        # Check that a verification code exists
        if not profile.verification_code:
            return Response(
                {'error': 'No verification code found. Please request a new code.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the code has expired
        if profile.verification_code_created_at:
            age = timezone.now() - profile.verification_code_created_at

            if age.total_seconds() > 600:  # 10 minutes
                return Response(
                    {'error': 'Verification code has expired. Please request a new code.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Check the code
        if code != profile.verification_code:
            return Response(
                {'error': 'Invalid verification code.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verification successful
        profile.is_verified = True
        profile.verification_code = None
        profile.verification_code_created_at = None
        profile.save()

        return Response(
            {'message': 'Email verified successfully.'},
            status=status.HTTP_200_OK
        )

# 3. User Profile Endpoint (View/Update Logged-in User Info)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# 4. Lifestyle Preferences Endpoint
class PreferencesView(generics.RetrieveUpdateAPIView):
    queryset = Preferences.objects.none()
    serializer_class = PreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Automatically creates preferences object for user if none exists
        preferences, _ = Preferences.objects.get_or_create(user=self.request.user)
        return preferences

# 5. Room Listings Endpoints (List all or Create new)
class RoomListingListCreateView(generics.ListCreateAPIView):
    queryset = RoomListing.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = RoomListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class RoomListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomListing.objects.all()
    serializer_class = RoomListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return RoomListing.objects.filter(is_active=True)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only edit your own listings."
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only delete your own listings."
            )

        instance.delete()


