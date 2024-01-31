from django.db import models
from django.core.validators import MinLengthValidator


class Offre(models.Model):
    Ofr_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=16)
    Apl_numero = models.ForeignKey('appels.Appel_d_Offre', on_delete=models.CASCADE)
    Ent_numero = models.ForeignKey('entreprises.Entreprise', on_delete=models.CASCADE)
    Ofr_description = models.TextField()
    Ofr_specifications = models.TextField()
    Ofr_montant = models.FloatField()
    Ofr_date = models.DateField(auto_now_add=True)
    Ofr_evaluation = models.FloatField(null=True)
    Ofr_document = models.ImageField(upload_to='Documents/Offre/')
    Ofr_statut = models.CharField(max_length=24, choices=[
        ('EN_EVALUATION', 'En évaluation'),
        ('ACCEPTEE', 'Acceptée'),
        ('REJETEE', 'Rejetée'),
    ], default = 'EN_EVALUATION')
    Ofr_conditions = models.ManyToManyField('appels.Condition', through='Evaluation1')
    
    def __str__(self):
        return f"{self.Ofr_numero}"


class Contrat(models.Model):
    Cnt_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=16)
    Ofr_numero = models.OneToOneField('Offre', on_delete=models.CASCADE)
    Cnt_type = models.CharField(max_length=48)
    Cnt_occurence = models.CharField(max_length=20, choices=[
        ('RENOUVELABLE', 'Renouvelable'),
        ('NON_RENOUVELABLE', 'Non renouvelable'),
    ])
    Cnt_dateDebut = models.DateField()
    Cnt_modeResiliation = models.CharField(max_length=96)
    Cnt_statut = models.CharField(max_length=20, choices=[
        ('EN_VALIDATION', 'En validation'),
        ('VALIDE', 'Validé'),
        ('INVALIDE', 'Invalidé'),
        ('EN_COURS', 'En cours'),
        ('RESILIE', 'Résilié'),
        ('ACHEVE', 'Achevé'),
    ], default = 'EN_VALIDATION')
    Cnt_indicateurs = models.ManyToManyField('Indicateur', through='Evaluation2')
    
    def __str__(self):
        return f"{self.Cnt_numero}"


class Version(models.Model):
    Vrs_id = models.AutoField(primary_key=True)
    Cnt_numero = models.ForeignKey('Contrat', on_delete=models.CASCADE)
    Vrs_description = models.TextField()
    Vrs_moment = models.DateTimeField(null=True, blank=True)
    Vrs_dateFin = models.DateField()
    Vrs_document = models.ImageField(upload_to='Documents/Contrat', null=True, blank=True)
    Vrs_modePaiement = models.CharField(max_length=96)
    Vrs_statut = models.CharField(max_length=20, choices=[
        ('EN_VALIDATION', 'En validation'),
        ('INVALIDE', 'Invalidé'),
        ('VALIDE', 'Validé'),
    ], default = 'EN_EVALUATION')
    
    def __str__(self):
        return f"{self.Cnt_numero} {self.Vrs_id}"


class Indicateur(models.Model):
    Ind_id = models.AutoField(primary_key=True)
    Ind_intitule = models.CharField(max_length=32)
    Ind_ponderation = models.IntegerField()
    
    def __str__(self):
        return f"{self.Ind_intitule}"


class Evaluation2(models.Model):
    Evl2_id = models.AutoField(primary_key=True)
    Cnt_numero = models.ForeignKey('Contrat', on_delete=models.CASCADE)
    Ind_id = models.ForeignKey('Indicateur', on_delete=models.CASCADE)
    Evl2_note = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Cnt_numero', 'Ind_id'], name='evaluation2_pk')
        ]
    
    def __str__(self):
        return f"{self.Cnt_numero} {self.Ind_id}"


class Etape2(models.Model):
    Etp2_id = models.AutoField(primary_key=True)
    Cnt_numero = models.ForeignKey('Contrat', on_delete=models.CASCADE)
    Etp2_titre = models.CharField(max_length=48)
    Etp2_description = models.TextField()
    Etp2_objectifs = models.TextField()
    Etp2_datePrevue = models.DateField()
    Etp2_dateExecution = models.DateField(null=True, blank=True)
    Etp2_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ])
    
    def __str__(self):
        return f"{self.Cnt_numero} {self.Etp2_id}"


class Paiement(models.Model):
    Pmt_numero = models.CharField(primary_key=True, validators=[MinLengthValidator(8)], max_length=100)
    Cnt_numero = models.ForeignKey('Contrat', on_delete=models.CASCADE)
    Pmt_mode = models.CharField(max_length=24)
    Pmt_description = models.TextField()
    Pmt_montant = models.FloatField()
    Pmt_date = models.DateField()
    Pmt_document = models.ImageField(upload_to='Documents/Paiement', blank=True, null=True)
    Pmt_statut = models.CharField(max_length=20, choices=[
        ('EN_VALIDATION', 'En validation'),
        ('INVALIDE', 'Invalidé'),
        ('VALIDE', 'Validé'),
    ], default = 'EN_EVALUATION')
    
    def __str__(self):
        return f"{self.Pmt_numero}"


class Evaluation1(models.Model):
    Evl1_id = models.AutoField(primary_key=True)
    Cnd_id = models.ForeignKey('appels.Condition', on_delete=models.CASCADE)
    Ofr_numero = models.ForeignKey('Offre', on_delete=models.CASCADE)
    Evl1_note = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Cnd_id', 'Ofr_numero'], name='evaluation1_pk')
        ]
    
    def __str__(self):
        return f"{self.Ofr_numero} {self.Cnd_id}"