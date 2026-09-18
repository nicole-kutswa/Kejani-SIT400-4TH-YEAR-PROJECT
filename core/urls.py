from django.urls import path
from .views import (
    RegisterView, 
    LoginView,
    VerifyEmailView,
    UserProfileView, 
    PreferencesView, 
    RoomListingListCreateView,
    RoomListingDetailView,
    MatchesView


)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('preferences/', PreferencesView.as_view(), name='user-preferences'),
    path('listings/', RoomListingListCreateView.as_view(), name='room-listings'),
    path('listings/<int:pk>/', RoomListingDetailView.as_view(), name='room-listing-detail'),
    path('matches/', MatchesView.as_view(), name='matches'),
]