"""
URL configuration for passport_tracking_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Redirect root to login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('application/', include('applications.urls')),
    path('officer/', include('officer.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('ml_prediction/', include('ml_prediction.urls')),
    path('notifications/', include('notifications.urls')),  # ⭐ ADD THIS

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Passport Tracking System Admin"
admin.site.site_title = "Passport Admin Portal"
admin.site.index_title = "Welcome to Passport Tracking Administration"
