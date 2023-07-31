from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('offer/', views.OfferView.as_view(), name='offer'),
    path('contract/', views.ContractView.as_view(), name='contract')
]