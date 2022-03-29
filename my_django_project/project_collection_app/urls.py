from django.urls import path
#from .views import ProjectViews
from .views import GithubProjectList
from .views import GithubProjectDetail


urlpatterns = [
    path('github_projects/', GithubProjectList.as_view()),
    path('github_projects/<int:pk>', GithubProjectDetail.as_view())
]

#urlpatterns = [
    #path('github_projects/', ProjectViews.as_view()),
    #path('github_projects/<int:id>', ProjectViews.as_view())
#]