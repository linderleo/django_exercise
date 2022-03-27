from rest_framework import serializers
from .models import GithubProject

class GithubProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubProject
        fields = ('__all__')