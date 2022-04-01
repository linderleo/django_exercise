from rest_framework import generics
from .models import GithubProject, Webhook
from .serializers import GithubProjectSerializer, WebhookSerializer
from rest_framework import permissions
from project_collection_app.permissions import IsOwnerOrReadOnly
import requests
import json

class GithubProjectList(generics.ListCreateAPIView):
    queryset = GithubProject.objects.all()
    serializer_class = GithubProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        def webhook_call(payload, url: str):
            try:
                print(f"LÄHTEE KUTSU: {url}")
                r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                print(r)
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something else happened: {err}")

        serializer.save(owner=self.request.user)
        hooks = Webhook.objects.values_list('url')
        [webhook_call(serializer.data, hook[0]) for hook in hooks]

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

