from django.urls import path
from . import views


urlpatterns = [
    path('project/', views.ProjectView.as_view(), name='project'),
    path('projets/', views.ProjetsView.as_view(), name='projets'),
    path('projet/', views.ProjetView.as_view(), name='projet')
]