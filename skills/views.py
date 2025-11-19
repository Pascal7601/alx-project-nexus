from rest_framework import generics
from . import serializers
from .models import Skill

class SkillListCreateView(generics.ListCreateAPIView):
    """GET: List all skills
       POST: Create a new skill
    """
    serializer_class = serializers.SkillSerializer
    queryset = Skill.objects.all()

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Retrieve a skill
       PUT/PATCH: Update a skill
       DELETE: Delete a skill
    """
    serializer_class = serializers.SkillSerializer
    queryset = Skill.objects.all()