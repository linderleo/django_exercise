from django.urls import path
from .views import ProjectViews

urlpatterns = [
    path('github_projects/', ProjectViews.as_view()),
    path('github_projects/<int:id>', ProjectViews.as_view())
]