from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Prediction, ProcessingHistory
from applications.models import Application
from django.db.models import Avg, Count
import json


@staff_member_required
def ml_analytics(request):
    """ML Analytics Dashboard - Only for admin/staff"""
    
    # Get statistics
    total_predictions = Prediction.objects.count()
    completed_apps = Application.objects.filter(current_status='delivered').count()
    
    # Calculate average predicted days
    avg_predicted = Prediction.objects.aggregate(Avg('predicted_days'))
    avg_predicted_days = int(avg_predicted['predicted_days__avg'] or 0)
    
    # Model accuracy (hardcoded - you can calculate dynamically)
    model_accuracy = 88  # From training
    
    # Recent predictions with accuracy calculation
    recent_predictions_raw = Prediction.objects.select_related('application').order_by('-prediction_date')[:20]
    
    # Add accuracy info to each prediction
    recent_predictions = []
    for pred in recent_predictions_raw:
        pred_dict = {
            'prediction': pred,
            'application': pred.application,
            'predicted_days': pred.predicted_days,
            'actual_days': None,
            'difference': None,
            'is_accurate': None,
        }
        
        # Calculate accuracy if completed
        if pred.application.actual_completion_date:
            actual_days = pred.application.get_processing_days()
            difference = pred.predicted_days - actual_days
            
            pred_dict['actual_days'] = actual_days
            pred_dict['difference'] = difference
            pred_dict['is_accurate'] = abs(difference) < 5
        
        recent_predictions.append(pred_dict)
    
    # Chart data - Last 10 completed applications
    completed = Application.objects.filter(
        current_status='delivered',
        actual_completion_date__isnull=False
    ).order_by('-actual_completion_date')[:10]
    
    chart_labels = [app.application_number for app in completed]
    predicted_data = [app.predicted_completion_days or 0 for app in completed]
    actual_data = [app.get_processing_days() for app in completed]
    
    context = {
        'total_predictions': total_predictions,
        'model_accuracy': model_accuracy,
        'avg_predicted_days': avg_predicted_days,
        'completed_apps': completed_apps,
        'recent_predictions': recent_predictions,
        'chart_labels': json.dumps(chart_labels),
        'predicted_data': json.dumps(predicted_data),
        'actual_data': json.dumps(actual_data),
    }
    
    return render(request, 'ml_prediction/analytics.html', context)