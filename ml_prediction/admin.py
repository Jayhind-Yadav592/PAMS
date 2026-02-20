from django.contrib import admin
from .models import ProcessingHistory, Prediction

@admin.register(ProcessingHistory)
class ProcessingHistoryAdmin(admin.ModelAdmin):
    list_display = ['application', 'actual_processing_days', 'city', 'completion_date']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['application', 'predicted_days', 'prediction_date']
