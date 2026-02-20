from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('verify/<int:stage_id>/', views.verify_application, name='verify_application'),
]
