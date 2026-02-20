from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from applications.models import Application, ApplicationStage
from accounts.models import User
from django.db.models import Count, Avg
from datetime import datetime, timedelta


@staff_member_required
def admin_dashboard(request):
    """Admin analytics dashboard"""
    # Statistics
    total_apps = Application.objects.count()
    pending_apps = Application.objects.filter(
        current_status__in=['submitted', 'document_verification', 'police_verification']
    ).count()
    completed_apps = Application.objects.filter(current_status='delivered').count()
    rejected_apps = Application.objects.filter(current_status='rejected').count()
    
    # Recent applications
    recent_apps = Application.objects.all()[:10]
    
    # Monthly stats
    last_30_days = datetime.now().date() - timedelta(days=30)
    monthly_apps = Application.objects.filter(
        submission_date__gte=last_30_days
    ).count()
    
    context = {
        'total_apps': total_apps,
        'pending_apps': pending_apps,
        'completed_apps': completed_apps,
        'rejected_apps': rejected_apps,
        'recent_apps': recent_apps,
        'monthly_apps': monthly_apps,
    }
    return render(request, 'admin_panel/admin_dashboard.html', context)
