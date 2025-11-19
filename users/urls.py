from django.urls import path
from . import views

urlpatterns = [
    path("users/register/", views.UserCreateView.as_view()),
    path("users/me/", views.UserDetailView.as_view()),
    path("profile/candidate/", views.CandidateDetailView.as_view()),
    path("companies/", views.CompanyListCreateView.as_view()),
    path("companies/<str:pk>/", views.CompanyRetrieveUpdateDestroyView.as_view()),
]