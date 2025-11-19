from django.urls import path
from . import views

urlpatterns = [
    path("", views.SkillListCreateView.as_view()),
    path("<str:pk>/", views.SkillDetailView.as_view()),
]