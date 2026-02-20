from django.contrib import admin
from .models import Application, Document, ApplicationStage

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'full_name', 'application_type', 'current_status', 'submission_date']
    list_filter = ['application_type', 'current_status', 'submission_date']
    search_fields = ['application_number', 'full_name', 'email']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'document_type', 'verified', 'uploaded_at']
    list_filter = ['document_type', 'verified']

@admin.register(ApplicationStage)
class ApplicationStageAdmin(admin.ModelAdmin):
    list_display = ['application', 'stage_name', 'status', 'assigned_officer']
    list_filter = ['status', 'stage_name']
