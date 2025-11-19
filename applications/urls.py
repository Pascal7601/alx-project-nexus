from django.urls import path
from . import views

urlpatterns = [    
    path('applications/my/', views.CandidateApplicationListView.as_view(), name='my-applications'),
    path('applications/<uuid:pk>/', views.ApplicationStatusUpdateView.as_view(), name='update-application-status'),
]