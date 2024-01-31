from django.db import models
from django.core.validators import MinLengthValidator


class Appel_a_Manifestation(models.Model):
    Ami_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=16)
    Ami_titre = models.CharField(max_length=96)
    Ami_description = models.TextField()
    Ami_dateDebut = models.DateField()
    Ami_dateFin = models.DateField()
    Ami_delaiValidite = models.IntegerField()
    Ami_document = models.ImageField(upload_to='Documents/AppelaManifestation/')
    Ami_coordonnees = models.CharField(max_length=160)
    Ami_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINE', 'Terminé'),
    ])
    Ami_Entreprises = models.ManyToManyField('entreprises.Entreprise', through='entreprises.Manifestation')
    
    def __str__(self):
        return f"{self.Ami_numero} {self.Ami_titre}"


class Appel_d_Offre(models.Model):
    Apl_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=16)
    Pjt_numero = models.ForeignKey('projets.Projet_d_Approvisionnement', on_delete=models.CASCADE)
    Apl_titre = models.CharField(max_length=96)
    Apl_description = models.TextField()
    Apl_exigences = models.TextField()
    Apl_dateDebut = models.DateField()
    Apl_dateFin = models.DateField()
    Apl_document = models.ImageField(upload_to='Documents/AppeldOffre/')
    Apl_coordonnees = models.CharField(max_length=160)
    Apl_budget = models.FloatField()
    Apl_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
    ])
    Apl_criteres = models.ManyToManyField('Critere', through='Condition')
    Apl_prestations = models.ManyToManyField('Prestation1', through='Allocation3')
    
    def __str__(self):
        return f"{self.Apl_numero} {self.Apl_titre}"


class Prestation1(models.Model):
    Ptn1_id = models.AutoField(primary_key=True)
    Ctg_id = models.ForeignKey('entreprises.Categorie', on_delete=models.CASCADE)
    Ptn1_description = models.TextField()
    Ptn1_delai = models.IntegerField()
    Ptn1_quantite = models.IntegerField()
    Ptn1_budget = models.FloatField()
    
    def __str__(self):
        return f"{self.Ptn1_description} {self.Ptn1_delai} jrs {self.Ptn1_quantite} (qté) {self.Ptn1_budget} francs"


class Critere(models.Model):
    Crt_id = models.AutoField(primary_key=True)
    Crt_intitule = models.CharField(max_length=32)
    Crt_ponderation = models.IntegerField()
    
    def __str__(self):
        return f"{self.Crt_intitule}"


class Condition(models.Model):
    Cnd_id = models.AutoField(primary_key=True)
    Apl_numero = models.ForeignKey('Appel_d_Offre', on_delete=models.CASCADE)
    Crt_id = models.ForeignKey('Critere', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Apl_numero', 'Crt_id'], name='condition_pk')
        ]
    
    def __str__(self):
        return f"{self.Apl_numero} {self.Crt_id}"


class Allocation3(models.Model):
    Alc3_id = models.AutoField(primary_key=True)
    Apl_numero = models.ForeignKey('Appel_d_Offre', on_delete=models.CASCADE)
    Ptn1_id = models.ForeignKey('Prestation1', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Apl_numero', 'Ptn1_id'], name='allocation3_pk')
        ]
    
    def __str__(self):
        return f"{self.Apl_numero} {self.Ptn1_id}"