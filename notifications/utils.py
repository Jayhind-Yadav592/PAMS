"""
Notification Utility Functions
Send notifications to users
"""

from .models import Notification
from django.core.mail import send_mail
from django.conf import settings


def create_notification(user, title, message, application=None, notification_type='system'):
    """
    Create a notification for user
    
    Args:
        user: User object
        title: Notification title
        message: Notification message
        application: Application object (optional)
        notification_type: 'system', 'email', 'sms'
    
    Returns:
        Notification object
    """
    notification = Notification.objects.create(
        user=user,
        application=application,
        title=title,
        message=message,
        notification_type=notification_type
    )
    
    # Send email if type is email
    if notification_type == 'email':
        send_email_notification(user, title, message)
    
    return notification


def send_email_notification(user, title, message):
    """
    Send email notification
    Configure email settings in settings.py first
    """
    try:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        print(f"✉️ Email sent to {user.email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")


def notify_application_submitted(application):
    """Notify when application is submitted"""
    user = application.user
    title = "Application Submitted Successfully"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Your passport application has been submitted successfully.
    
    Application Number: {application.application_number}
    Type: {application.get_application_type_display()}
    Expected Processing Time: {application.predicted_completion_days} days
    Expected Completion: {application.expected_completion_date}
    
    You can track your application status anytime.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_document_verified(application):
    """Notify when documents are verified"""
    user = application.user
    title = "Documents Verified"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Your documents have been verified successfully.
    
    Application Number: {application.application_number}
    Status: Document Verification Completed
    Next Step: Police Verification
    
    Your application is now moving to the next stage.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_police_verification_started(application):
    """Notify when police verification starts"""
    user = application.user
    title = "Police Verification Started"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Police verification for your application has been initiated.
    
    Application Number: {application.application_number}
    
    A police officer will visit your address for verification.
    Please keep your documents ready.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_police_verification_completed(application):
    """Notify when police verification is completed"""
    user = application.user
    title = "Police Verification Completed"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Police verification has been completed successfully.
    
    Application Number: {application.application_number}
    Status: Police Verification Completed
    Next Step: Final Approval
    
    Your application is now under final review.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_application_approved(application):
    """Notify when application is approved"""
    user = application.user
    title = "🎉 Application Approved!"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Congratulations! Your passport application has been approved.
    
    Application Number: {application.application_number}
    Status: Approved
    Next Step: Printing
    
    Your passport is now being processed for printing.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_application_rejected(application, reason=""):
    """Notify when application is rejected"""
    user = application.user
    title = "Application Rejected"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    We regret to inform you that your passport application has been rejected.
    
    Application Number: {application.application_number}
    Status: Rejected
    
    Reason: {reason or "Please contact the passport office for details."}
    
    You may reapply after addressing the issues.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_printing_started(application):
    """Notify when passport printing starts"""
    user = application.user
    title = "Passport Printing Started"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Your passport is now being printed.
    
    Application Number: {application.application_number}
    Status: Printing in Progress
    
    Your passport will be dispatched soon.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_application_dispatched(application):
    """Notify when passport is dispatched"""
    user = application.user
    title = "📦 Passport Dispatched"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Great news! Your passport has been dispatched.
    
    Application Number: {application.application_number}
    Status: Dispatched
    
    Expected Delivery: 3-5 business days
    
    You will receive it at your registered address soon.
    
    Thank you!
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def notify_application_delivered(application):
    """Notify when passport is delivered"""
    user = application.user
    title = "✅ Passport Delivered"
    message = f"""
    Dear {user.get_full_name() or user.username},
    
    Congratulations! Your passport has been delivered successfully.
    
    Application Number: {application.application_number}
    Status: Delivered
    Delivery Date: {application.actual_completion_date}
    
    Thank you for using our services!
    
    Passport Services
    """
    
    create_notification(user, title, message, application, 'system')


def get_user_notifications(user, limit=10, unread_only=False):
    """
    Get user's notifications
    
    Args:
        user: User object
        limit: Number of notifications to return
        unread_only: Return only unread notifications
    
    Returns:
        QuerySet of notifications
    """
    notifications = Notification.objects.filter(user=user)
    
    if unread_only:
        notifications = notifications.filter(is_read=False)
    
    return notifications[:limit]


def mark_notification_as_read(notification_id, user):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=user)
        notification.is_read = True
        notification.save()
        return True
    except Notification.DoesNotExist:
        return False


def mark_all_as_read(user):
    """Mark all notifications as read for user"""
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    return True