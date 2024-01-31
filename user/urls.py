from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='signin'),
    path('profil/', views.ProfilView.as_view(), name='profil'),
    path('change/', views.ChangeView.as_view(), name='change'),
    path('changed/', PasswordChangeDoneView.as_view(template_name = 'changed.html'), name='changed')
]
