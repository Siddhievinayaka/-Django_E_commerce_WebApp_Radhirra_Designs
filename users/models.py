from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    # Add any other custom fields you might need for your user here
    # For example, you might want to add a phone number or a date of birth directly to the user model

    USERNAME_FIELD = "email"  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = [
        "username"
    ]  # 'username' will still be required for superuser creation, but not for login

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    profile_pic = CloudinaryField(
        "image", default="profile_pics/default.png", blank=True, null=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ""
        return url
