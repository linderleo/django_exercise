from rest_framework import generics
from .models import GithubProject
from .serializers import GithubProjectSerializer
from rest_framework import permissions
from project_collection_app.permissions import IsOwnerOrReadOnly

class GithubProjectList(generics.ListCreateAPIView):
    queryset = GithubProject.objects.all()
    serializer_class = GithubProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GithubProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GithubProject.objects.all()
    serializer_class = GithubProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

