from django.db import models


class ProcessingHistory(models.Model):
    """Historical data for ML"""
    application = models.OneToOneField('applications.Application', on_delete=models.CASCADE)
    actual_processing_days = models.IntegerField()
    application_type = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    submission_month = models.IntegerField()
    workload_at_submission = models.IntegerField(default=0)
    completion_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Processing Histories"
    
    def __str__(self):
        return f"{self.application.application_number} - {self.actual_processing_days} days"


class Prediction(models.Model):
    """Store ML predictions"""
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE)
    predicted_days = models.IntegerField()
    confidence_score = models.FloatField(default=0.0)
    prediction_date = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default='v1.0')
    
    def __str__(self):
        return f"{self.application.application_number} - {self.predicted_days} days"
