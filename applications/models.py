from django.db import models
from accounts.models import User
from datetime import datetime, timedelta


class Application(models.Model):
    """Passport Application Model"""
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('document_verification', 'Document Verification'),
        ('police_verification', 'Police Verification'),
        ('approved', 'Approved'),
        ('printing', 'Printing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
    )
    
    TYPE_CHOICES = (
        ('new', 'New Passport'),
        ('renewal', 'Renewal'),
        ('reissue', 'Re-issue'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_number = models.CharField(max_length=20, unique=True)
    application_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')
    submission_date = models.DateTimeField(auto_now_add=True)
    predicted_completion_days = models.IntegerField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    
    priority = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.application_number} - {self.full_name}"


class Document(models.Model):
    """Documents uploaded"""
    DOCUMENT_TYPES = (
        ('photo', 'Passport Photo'),
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('dob_proof', 'Date of Birth Proof'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.application.application_number} - {self.get_document_type_display()}"


class ApplicationStage(models.Model):
    """Tracks each stage"""
    STAGE_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='stages')
    stage_name = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STAGE_STATUS, default='pending')
    assigned_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.application.application_number} - {self.stage_name}"
