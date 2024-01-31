from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    Ent_numero = models.ForeignKey('entreprises.Entreprise', on_delete=models.SET_DEFAULT, default="1613978901")
    Usr_fonction = models.CharField(max_length=64)
    Usr_telephone = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex=r'^\+?\d{8,15}$',
            message="Le numéro de téléphone doit être au format valide."
        ), MinLengthValidator(8)
    ])
    Usr_profil = models.ImageField(upload_to='Images/Profils/', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Utilisateurs"
        
    def __str__(self):
        return f"{self.username}"