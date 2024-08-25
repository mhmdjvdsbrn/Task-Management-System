from rest_framework import serializers
from .models import Task

class TaskSelectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'user']
        read_only_fields = ['user'] 

class TaskServicesSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False, default="in_progress")

