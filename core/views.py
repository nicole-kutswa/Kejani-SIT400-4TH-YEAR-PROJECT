from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

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