from rest_framework import serializers
from .models import GithubProject

class GithubProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubProject
        fields = ('__all__')

        extra_kwargs = {
            'owner': { 'read_only': True }
        }