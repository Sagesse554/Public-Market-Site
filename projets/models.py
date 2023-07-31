from django.db import models
from django.core.validators import MinLengthValidator


class Projet_d_Approvisionnement(models.Model):
    Pjt_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=16)
    Pjt_titre = models.CharField(max_length=96)
    Pjt_description = models.TextField()
    Pjt_dateDebut = models.DateField()
    Pjt_dateFin = models.DateField()
    Pjt_objectifs = models.TextField()
    Pjt_document = models.FileField(upload_to='Documents/Projet d\'Approvisionnement')
    Pjt_budget = models.FloatField()
    Pjt_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
    ])
    
    def __str__(self):
        return f"{self.Pjt_numero}"

class Etape1(models.Model):
    Etp1_id = models.AutoField(primary_key=True)
    Pjt_numero = models.ForeignKey('Projet_d_Approvisionnement', on_delete=models.CASCADE)
    Etp1_titre = models.CharField(max_length=48)
    Etp1_description = models.TextField()
    Etp1_objectifs = models.TextField()
    Etp1_dateDebut = models.DateField()
    Etp1_dateFin = models.DateField()
    Etp1_budget = models.FloatField()
    Etp1_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ])
    
    def __str__(self):
        return f"{self.Pjt_numero} {self.Etp1_titre}"