from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('signout/', views.LogoutView, name='signout')
]
