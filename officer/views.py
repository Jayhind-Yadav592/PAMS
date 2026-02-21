from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from applications.models import Application, ApplicationStage
from django.utils import timezone
from notifications.utils import (  # ⭐ NEW
    notify_document_verified,
    notify_police_verification_started,
    notify_police_verification_completed,
    notify_application_approved,
    notify_application_rejected
)


@login_required
def officer_dashboard(request):
    """Officer dashboard"""
    if not (request.user.is_police_officer or request.user.is_rpo_officer or request.user.is_staff):
        messages.error(request, 'Access denied. Officer credentials required.')
        return redirect('dashboard')
    
    # Get applications based on role
    if request.user.is_police_officer:
        pending = ApplicationStage.objects.filter(
            stage_name='Police Verification',
            status='pending'
        )
    else:
        pending = ApplicationStage.objects.filter(
            status='pending'
        )
    
    context = {
        'pending_count': pending.count(),
        'pending_stages': pending[:10],
    }
    return render(request, 'officer/officer_dashboard.html', context)


@login_required
def verify_application(request, stage_id):
    """Verify application stage"""
    stage = get_object_or_404(ApplicationStage, id=stage_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        if action == 'approve':
            stage.status = 'completed'
            stage.end_time = timezone.now()
            stage.remarks = remarks
            stage.save()
            
            # Update application status
            application = stage.application
            
            if stage.stage_name == 'Document Verification':
                application.current_status = 'police_verification'
                notify_document_verified(application)  # ⭐ NOTIFY
                
            elif stage.stage_name == 'Police Verification':
                application.current_status = 'approved'
                notify_police_verification_completed(application)  # ⭐ NOTIFY
                notify_application_approved(application)  # ⭐ NOTIFY
                
            application.save()
            
            messages.success(request, f'Stage "{stage.stage_name}" approved successfully!')
        
        elif action == 'reject':
            stage.status = 'rejected'
            stage.remarks = remarks
            stage.save()
            
            stage.application.current_status = 'rejected'
            stage.application.save()
            
            notify_application_rejected(stage.application, remarks)  # ⭐ NOTIFY
            
            messages.warning(request, f'Application rejected.')
        
        return redirect('officer_dashboard')
    
    return render(request, 'officer/verify_application.html', {'stage': stage})