from django.urls import path
from . import views

urlpatterns = [    
    path('my/', views.CandidateApplicationListView.as_view(), name='my-applications'),
    path('<uuid:pk>/', views.ApplicationStatusUpdateView.as_view(), name='update-application-status'),
]