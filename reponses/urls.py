from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('offer/', views.OfferView.as_view(), name='offer'),
    path('contract/', views.ContractView.as_view(), name='contract'),
    path('offres/', views.OffresView.as_view(), name='offres'),
    path('contrats/', views.ContratsView.as_view(), name='contrats'),
    path('offre/', views.OffreView.as_view(), name='offre'),
    path('contrat/', views.ContratView.as_view(), name='contrat')
]