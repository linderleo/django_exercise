from django.contrib import admin
from .models import GithubProject, Webhook

admin.site.register(GithubProject)
admin.site.register(Webhook)


