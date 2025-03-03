import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from reward_system import settings


class User(AbstractUser):
    """
    Custom User model extending Django's built-in user model.
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # User profile image
    points = models.PositiveIntegerField(default=0)  # Reward points

    def __str__(self):
        return self.username


class Application(models.Model):
    """
    Model representing an Android application in the reward system.
    """
    name = models.CharField(max_length=255)  # Name of the application
    link_app = models.URLField(unique=True)  # Link to the application details
    download_link = models.URLField(unique=True)  # Direct link to download the app
    points = models.PositiveIntegerField()  # Points awarded for downloading the app
    category = models.CharField(max_length=255, choices=[
        ('social', 'Social Networks'),
        ('game', 'Game'),
        ('productivity', 'Productivity')
    ])  # Application category

    default_logo = models.CharField(max_length=255, blank=True, null=True)
    # Predefined logo path if no custom image is uploaded

    custom_logo = models.ImageField(upload_to='app_logos/', blank=True, null=True)
    # Custom logo uploaded by the admin (stored in 'media/app_logos/')

    def get_logo(self):
        """
        Returns the correct logo based on priority.
        """
        if self.custom_logo:  # 1. Check if a custom logo is set
            return self.custom_logo.url
        elif self.default_logo:  # 2. Check if a default logo is set
            return self.default_logo
        else:  # 3. Use a generic icon if no logo is set
            return os.path.join(settings.STATIC_URL, "images/default_app_logo.png")

    def __str__(self):
        """
        Returns a string representation of the application.
        """
        return f"{self.name} ({self.points} points)"


class Task(models.Model):
    """
    Model representing a user task (proof of app download).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who completed the task
    application = models.ForeignKey(Application, on_delete=models.CASCADE)  # Associated application
    screenshot = models.ImageField(upload_to='screenshots/')  # Proof of app download
    is_approved = models.BooleanField(default=False)  # Admin validation status
    created_at = models.DateTimeField(auto_now=True)  # Task creation date

    def __str__(self):
        return f"Task by {self.user} for {self.application} - {'Approved' if self.is_approved else 'Pending'}"
