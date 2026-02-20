from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User Model with role-based access control
    Extends Django's built-in AbstractUser
    """
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('police', 'Police Officer'),
        ('rpo', 'RPO Officer'),
        ('admin', 'Admin'),
    )
    
    # Additional fields
    phone = models.CharField(max_length=15, blank=True, help_text="Contact number")
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='citizen',
        help_text="User role in the system"
    )
    address = models.TextField(blank=True, help_text="Residential address")
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Profile picture (optional)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True,
        help_text="Profile photo"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_address(self):
        """Return complete address"""
        parts = [self.address, self.city, self.state, self.pincode]
        return ', '.join(filter(None, parts))
    
    @property
    def is_citizen(self):
        return self.role == 'citizen'
    
    @property
    def is_police_officer(self):
        return self.role == 'police'
    
    @property
    def is_rpo_officer(self):
        return self.role == 'rpo'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
