from django.db import models
from django.contrib.auth.models import User

# Extends standard Django User with Student-specific fields
class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    university = models.CharField(max_length=250)
    registration_number = models.CharField(
        max_length=100,
        unique=True
    )
    phone_number = models.CharField(max_length=15)

    # Email verification
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )
    verification_code_created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.university}"
# Roommate & Lifestyle Preferences for Matching
class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferred_location = models.CharField(max_length=200, default='', blank=True)
    cleanliness_level = models.IntegerField(default=3)  # Scale 1 to 5
    study_habits = models.CharField(max_length=50, default='Flexible', blank=True)
    smoking_allowed = models.BooleanField(default=False)
    guests_allowed = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Preferences"


    def __str__(self):
        return f"Preferences for {self.user.username}"

# Accommodation Listings
class RoomListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    total_rent = models.DecimalField(max_digits=10, decimal_places=2)
    rent_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    rooms_available = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - KES {self.rent_per_person}/mo"

# Create your models here.
