from django.urls import path
from . import views


urlpatterns = [
    path('project/', views.ProjectView.as_view(), name='project')
]