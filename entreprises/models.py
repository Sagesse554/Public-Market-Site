from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Entreprise(models.Model):
    Ent_numero = models.OneToOneField('Registre', on_delete=models.CASCADE, primary_key=True)
    Ent_dateCreation = models.DateField()
    Ent_evaluation = models.FloatField(null=True)
    
    def __str__(self):
        return f"{self.Ent_numero}"

class Registre(models.Model):
    Rgs_numero = models.CharField(max_length=16, primary_key=True, validators=[
        RegexValidator(
            regex=r'^\d{8,16}$',
            message="Le numéro d'identification fiscale doit être au format valide."
        ), MinLengthValidator(8)
    ])
    Rgs_denomination = models.CharField(max_length=64)
    Rgs_dateCreation = models.DateField()
    
    def __str__(self):
        return f"{self.Rgs_numero} {self.Rgs_denomination}"

class Manifestation(models.Model):
    Mnf_id = models.AutoField(primary_key=True)
    Ami_numero = models.ForeignKey('appels.Appel_a_Manifestation', on_delete=models.CASCADE)
    Ent_numero = models.ForeignKey('Entreprise', on_delete=models.CASCADE)
    Mnf_denomination = models.CharField(max_length=64)
    Mnf_moment = models.DateTimeField(auto_now_add=True)
    Mnf_logo = models.ImageField(upload_to='Images/Logos/', null=True, blank=True)
    Mnf_adresse = models.CharField(max_length=96)
    Mnf_telephone = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex=r'^\+?\d{8,15}$',
            message="Le numéro de téléphone doit être au format valide."
        )
    ])
    Mnf_email = models.EmailField()
    Mnf_siteWeb = models.CharField(max_length=48, null=True, blank=True)
    Mnf_document = models.FileField(upload_to='Documents/Manifestation/')
    Mnf_personnel = models.ManyToManyField('Personnel', through='Allocation1')
    Mnf_materiel = models.ManyToManyField('Materiel', through='Allocation2')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Ami_numero', 'Ent_numero'], name='manifestation_pk')
        ]
    
    def __str__(self):
        return f"{self.Ami_numero} {self.Ent_numero} {self.Mnf_denomination}"

class Reference(models.Model):
    Rfc_id = models.AutoField(primary_key=True)
    Ent_numero = models.ForeignKey('Entreprise', on_delete=models.CASCADE)
    Rfc_titre = models.CharField(max_length=96)
    Rfc_description = models.TextField()
    Rfc_client = models.CharField(max_length=64)
    Rfc_coordonnees = models.CharField(max_length=160)
    Rfc_document = models.FileField(upload_to='Documents/Reference')
    Rfc_typeContrat = models.CharField(max_length=48)
    Rfc_dateDebut = models.DateField()
    Rfc_dateFin = models.DateField()
    Rfc_montant = models.FloatField()
    Rfc_statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente'),
        ('TERMINEE', 'Terminée'),
    ])
    Rfc_categories = models.ManyToManyField('Categorie', through='Prestation3')
    
    def __str__(self):
        return f"{self.Ent_numero} {self.Rfc_titre}"

class Categorie(models.Model):
    Ctg_id = models.AutoField(primary_key=True)
    Ctg_titre = models.CharField(max_length=48)
    
    def __str__(self):
        return f"{self.Ctg_titre}"

class Prestation3(models.Model):
    Ptn3_id = models.AutoField(primary_key=True)
    Rfc_id = models.ForeignKey('Reference', on_delete=models.CASCADE)
    Ctg_id = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    Ptn3_description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Rfc_id', 'Ctg_id'], name='prestation3_pk')
        ]
    
    def __str__(self):
        return f"{self.Rfc_id} {self.Ctg_id} {self.Ptn3_description}"

class Personnel(models.Model):
    Prs_id = models.AutoField(primary_key=True)
    Prs_titre = models.CharField(max_length=48)
    Prs_description = models.TextField()
    
    def __str__(self):
        return f"{self.Prs_titre} {self.Prs_description}"

class Materiel(models.Model):
    Mtr_id = models.AutoField(primary_key=True)
    Mtr_titre = models.CharField(max_length=48)
    Mtr_description = models.TextField()
    
    def __str__(self):
        return f"{self.Mtr_titre} {self.Mtr_description}"

class Prestation2(models.Model):
    Ptn2_id = models.AutoField(primary_key=True)
    Ctg_id = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    Ptn2_description = models.TextField()
    Ptn2_delai = models.IntegerField()
    Ptn2_quantite = models.IntegerField()
    Ptn2_tarif = models.FloatField()

    def __str__(self):
        return f"{self.Ptn2_description} {self.Ptn2_delai} jrs {self.Ptn2_quantite} (qté) {self.Ptn2_tarif} francs"

class Allocation1(models.Model):
    Alc1_id = models.AutoField(primary_key=True)
    Mnf_id = models.ForeignKey('Manifestation', on_delete=models.CASCADE)
    Ptn2_id = models.ForeignKey('Prestation2', on_delete=models.CASCADE)
    Prs_id = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    Prs_quantite = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Mnf_id', 'Ptn2_id', 'Prs_id'], name='allocation1_pk')
        ]
    
    def __str__(self):
        return f"{self.Mnf_id} {self.Ptn2_id} {self.Prs_id}"

class Allocation2(models.Model):
    Alc2_id = models.AutoField(primary_key=True)
    Mnf_id = models.ForeignKey('Manifestation', on_delete=models.CASCADE)
    Ptn2_id = models.ForeignKey('Prestation2', on_delete=models.CASCADE)
    Mtr_id = models.ForeignKey('Materiel', on_delete=models.CASCADE)
    Mtr_quantite = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Mnf_id', 'Ptn2_id', 'Mtr_id'], name='allocation2_pk')
        ]
    
    def __str__(self):
        return f"{self.Mnf_id} {self.Ptn2_id} {self.Mtr_id}"