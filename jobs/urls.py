from django.urls import path
from . import views
from applications import views as application_views 

urlpatterns = [
    path("", views.JobListCreateView.as_view()),
    path("<str:pk>/", views.JobDetailView.as_view()),
    path('<uuid:job_id>/apply/', application_views.ApplyJobView.as_view()),
    path('<uuid:job_id>/applicants/', application_views.JobApplicantsListView.as_view()),
]