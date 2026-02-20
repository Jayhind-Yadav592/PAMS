from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('submit/', views.submit_application, name='submit_application'),
    path('track/<str:app_number>/', views.track_application, name='track_application'),
    path('upload/<str:app_number>/', views.upload_document, name='upload_document'),
]
