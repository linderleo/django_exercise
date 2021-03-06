from rest_framework import generics
from .models import GithubProject, Webhook
from .serializers import GithubProjectSerializer, WebhookSerializer
from rest_framework import permissions
from project_collection_app.permissions import IsOwnerOrReadOnly
import json
import httpx
import asyncio

class GithubProjectList(generics.ListCreateAPIView):
    serializer_class = GithubProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = GithubProject.objects.all()
        sort_by = self.request.query_params.get('sort_by')
        order = self.request.query_params.get('order')     
        if sort_by == "rating":
            if order == "desc":
                return queryset.order_by('-rating')
            else:
                return queryset.order_by('rating')
        elif sort_by == "created":
            if order == "desc":
                return queryset.order_by('-created')
            else:
                return queryset.order_by('created')
        else:
            return queryset

    # Below we do asynchronous webhook calls when we add a new project entry
    def perform_create(self, serializer):
        async def main(data: dict, urls: list[str]):
            async with httpx.AsyncClient() as client:
                for hook in urls:
                    print(f"Calling webhook: {hook}")
                    r = await client.post(hook, json=data)

        serializer.save(owner=self.request.user)
        hooks = Webhook.objects.values_list('url')
        asyncio.run(main(serializer.data, urls = [hook[0] for hook in hooks]))

class GithubProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GithubProject.objects.all()
    serializer_class = GithubProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

class WebhookList(generics.ListCreateAPIView):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WebhookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

