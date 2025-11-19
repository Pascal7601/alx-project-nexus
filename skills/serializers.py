from rest_framework import serializers
from .models import Skill

class SkillSerializer(serializers.ModelSerializer):
    """serializer for the Skill model"""
    class Meta:
        model = Skill
        fields = ["id", "name"]