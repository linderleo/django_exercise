from django.urls import path
#from .views import ProjectViews
from .views import GithubProjectList, GithubProjectDetail, WebhookList, WebhookDetail
#from .views import GithubProjectDetail


urlpatterns = [
    path('github_projects/', GithubProjectList.as_view(), name="github_projects"),
    path('github_projects/<int:pk>', GithubProjectDetail.as_view(), name="project_entry"),
    path('webhooks/', WebhookList.as_view(), name="webhooks"),
    path('webhooks/<int:pk>', WebhookDetail.as_view(), name="webhook_entry")
]

#urlpatterns = [
    #path('github_projects/', ProjectViews.as_view()),
    #path('github_projects/<int:id>', ProjectViews.as_view())
#]