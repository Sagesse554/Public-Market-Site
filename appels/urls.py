from django.urls import path
from . import views

urlpatterns = [
    path('manifestcall/', views.ManifestCallView.as_view(), name='manifestcall'),
    path('offercall/', views.OfferCallView.as_view(), name='offercall'),
    path('callmanifest/', views.CallManifestView.as_view(), name='callmanifest'),
    path('calloffer/', views.CallOfferView.as_view(), name='calloffer'),
    path('manifcall/', views.ManifCallView.as_view(), name='manifcall'),
    path('offcall/', views.OffCallView.as_view(), name='offcall')
]
