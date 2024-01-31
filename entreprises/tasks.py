from django.utils import timezone
from projets.models import Etape1

def update_etape_statuses():
    today = timezone.now().date()
    etapes = Etape1.objects.all()

    for etape in etapes:
        if etape.Etp1_statut == 'ANNULEE':
            continue

        if etape.Etp1_dateDebut > today:
            etape.Etp1_statut = 'EN_ATTENTE'
        elif etape.Etp1_dateFin < today:
            etape.Etp1_statut = 'TERMINEE'
        else:
            etape.Etp1_statut = 'EN_COURS'
        
        etape.save()