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
    PROPERTY_TYPES = [
        ('bedsitter', 'Bedsitter'),
        ('one_bedroom', '1 Bedroom'),
        ('two_bedroom', '2 Bedroom'),
        ('three_bedroom', '3 Bedroom'),
        ('shared_room', 'Shared Room'),
        ('other', 'Other'),
    ]

    GENDER_PREFERENCES = [
        ('any', 'Any'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default='bedsitter'
    )

    total_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    rent_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    current_occupants = models.PositiveIntegerField(default=1)

    spaces_available = models.PositiveIntegerField(default=1)

    furnished = models.BooleanField(default=False)

    utilities_included = models.BooleanField(default=False)

    gender_preference = models.CharField(
        max_length=10,
        choices=GENDER_PREFERENCES,
        default='any'
    )

    move_in_date = models.DateField(
        blank=True,
        null=True
    )

    amenities = models.TextField(
        blank=True,
        default=''
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        total_people = self.current_occupants + self.spaces_available

        if total_people > 0:
            self.rent_per_person = self.total_rent / total_people
        else:
            self.rent_per_person = self.total_rent

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - KES {self.rent_per_person}/person"

# Create your models here.
