from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, ApplicationStage, Document
from .forms import ApplicationForm, DocumentForm
from ml_prediction.predictor import predict_for_application
from notifications.utils import notify_application_submitted
from datetime import datetime, timedelta
import random


@login_required
def citizen_dashboard(request):
    """Citizen dashboard showing all applications"""
    applications = Application.objects.filter(user=request.user)
    unread_count = request.user.notifications.filter(is_read=False).count()
    context = {
        'applications': applications,
        'total_apps': applications.count(),
        'pending': applications.filter(current_status='submitted').count(),
        'completed': applications.filter(current_status='delivered').count(),
        "unread_count": unread_count,
    }
    return render(request, 'applications/citizen_dashboard.html', context)


@login_required
def submit_application(request):
    """Submit new passport application"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            
            # Generate application number
            year = datetime.now().year
            random_num = random.randint(100000, 999999)
            application.application_number = f"PSP{year}{random_num}"
            
            # ML Prediction
            try:
                predicted_days = predict_for_application(application)
                application.predicted_completion_days = predicted_days
                application.expected_completion_date = datetime.now().date() + timedelta(days=predicted_days)
            except:
                application.predicted_completion_days = 30
                application.expected_completion_date = datetime.now().date() + timedelta(days=30)
            
            application.save()
            
            # Create stages
            stages = [
                'Document Verification',
                'Police Verification',
                'Final Approval',
                'Printing',
                'Dispatch'
            ]
            for stage in stages:
                ApplicationStage.objects.create(
                    application=application,
                    stage_name=stage
                )
            
            # ⭐ SEND NOTIFICATION (NEW)
            notify_application_submitted(application)
            
            messages.success(request, f'Application submitted successfully! Number: {application.application_number}')
            return redirect('track_application', app_number=application.application_number)
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/submit_application.html', {'form': form})


@login_required
def track_application(request, app_number):
    """Track application status"""
    application = get_object_or_404(Application, application_number=app_number)
    
    # Check permission
    if application.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('citizen_dashboard')
    
    stages = application.stages.all().order_by('id')
    documents = application.documents.all()
    
    context = {
        'application': application,
        'stages': stages,
        'documents': documents,
    }
    return render(request, 'applications/track_application.html', context)


@login_required
def upload_document(request, app_number):
    """Upload additional documents"""
    application = get_object_or_404(Application, application_number=app_number, user=request.user)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('track_application', app_number=app_number)
    else:
        form = DocumentForm()
    
    return render(request, 'applications/upload_document.html', {'form': form, 'application': application})
