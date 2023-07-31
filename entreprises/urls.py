from django.urls import path
from . import views

urlpatterns = [
    path('manifest/', views.ManifestView.as_view(), name='manifest'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
    path('service/', views.Service2View.as_view(), name='service')
]