from django import forms
from django.forms import formset_factory
from entreprises.models import Registre, Entreprise, Manifestation, Reference, Prestation3, Prestation2, Personnel, Materiel, Allocation1, Allocation2, Categorie


class EnterpriseForm(forms.ModelForm):
    Ent_numero_entry = forms.CharField(max_length=16, required=True, label=("Ent_numero"), widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Numéro d'enterprise"}))
    Ent_dateCreation = forms.DateField(required=True, label=("Ent_dateCreation"), widget=forms.DateInput(attrs={"class": "form-control form-control-lg", "placeholder": "Date de création"}))

    class Meta:
        model = Entreprise
        fields = ['Ent_numero_entry', 'Ent_dateCreation']

    def clean_Ent_numero_entry(self):
        Ent_numero = self.cleaned_data.get('Ent_numero_entry')

        try:
            registre = Registre.objects.get(Rgs_numero=Ent_numero)
            if registre == Registre.objects.order_by('id').first() :
                raise forms.ValidationError("Veuillez voir l'administrateur pour un telle opération.")
            
        except Registre.DoesNotExist:
            raise forms.ValidationError("Une telle entreprise n'a jamais été enregistrée.")
        
        return Ent_numero
    
    def clean_Ent_dateCreation(self):
        Ent_numero = self.cleaned_data.get('Ent_numero_entry')
        Ent_dateCreation = self.cleaned_data.get('Ent_dateCreation')

        try:
            registre = Registre.objects.get(Rgs_numero=Ent_numero)
            if not registre.Rgs_dateCreation == Ent_dateCreation :
                raise forms.ValidationError("Vérifiez les informations de votre entreprise.")
        except Registre.DoesNotExist:
            pass
        
        return Ent_dateCreation


class ManifestForm(forms.ModelForm):

    class Meta:
        model = Manifestation
        fields = ['Mnf_denomination', 'Mnf_logo', 'Mnf_adresse', 'Mnf_telephone', 'Mnf_email', 'Mnf_siteWeb', 'Mnf_document']
        
        widgets = {
            'Mnf_denomination': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nom d\'entreprise'
            }),
            'Mnf_logo': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Mnf_adresse': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Adresse'
            }),
            'Mnf_telephone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Téléphone'
            }),
            'Mnf_email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'E-mail'
            }),
            'Mnf_siteWeb': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Site Web'
            }),
            'Mnf_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }


class ReferenceForm(forms.ModelForm):
    Rfc_categories = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control form-control-lg',
        }))

    class Meta:
        model = Reference
        fields = ['Rfc_titre', 'Rfc_description', 'Rfc_client', 'Rfc_coordonnees', 'Rfc_document', 'Rfc_typeContrat', 'Rfc_dateDebut', 'Rfc_dateFin', 'Rfc_montant', 'Rfc_statut', 'Rfc_categories']

        widgets = {
            'Rfc_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Rfc_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Rfc_client': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Client'
            }),
            'Rfc_coordonnees': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Coordonnées'
            }),
            'Rfc_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Rfc_typeContrat': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Type de Contrat'
            }),
            'Rfc_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Rfc_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Rfc_montant': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Montant'
            }),
            'Rfc_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
    
    def clean_Rfc_dateFin(self):
        Rfc_dateDebut = self.cleaned_data.get('Rfc_dateDebut')
        Rfc_dateFin = self.cleaned_data.get('Rfc_dateFin')

        if Rfc_dateFin <= Rfc_dateDebut :
            raise forms.ValidationError("Respectez l'ordre des dates !")
        
        return Rfc_dateFin
    
    def clean_Rfc_montant(self):
        Rfc_montant = self.cleaned_data.get('Rfc_montant')

        if Rfc_montant <= 0 :
            raise forms.ValidationError("Le montant ne peut être qu'un nombre positif !")
        
        return Rfc_montant


class Service3Form(forms.ModelForm):
    
    class Meta:
        model = Prestation3
        fields = ['Ctg_id', 'Ptn3_description']
        
        widgets = {
            'Ctg_id': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Ptn3_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            })
        }


Service3FormSet = formset_factory(Service3Form, extra=1)


class Allocation2Form(forms.ModelForm):
    
    class Meta:
        model = Allocation2
        fields = ['Mtr_id', 'Mtr_quantite']
        
        widgets = {
            'Mtr_id': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Mtr_quantite': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Quantité'
            })
        }

    def clean_Mtr_quantite(self):
        Mtr_quantite = self.cleaned_data.get('Mtr_quantite')

        if Mtr_quantite <= 0 :
            raise forms.ValidationError("La quantité ne peut être qu'un entier positif !")
        
        return Mtr_quantite


EquipmentFormSet = formset_factory(Allocation2Form, extra=1, can_delete=True)

class Allocation1Form(forms.ModelForm):
    
    class Meta:
        model = Allocation1
        fields = ['Prs_id', 'Prs_quantite']
        
        widgets = {
            'Prs_id': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Prs_quantite': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Quantité'
            })
        }

    def clean_Prs_quantite(self):
        Prs_quantite = self.cleaned_data.get('Prs_quantite')

        if Prs_quantite <= 0 :
            raise forms.ValidationError("La quantité ne peut être qu'un entier positif !")
        
        return Prs_quantite


StaffFormSet = formset_factory(Allocation1Form, extra=1, can_delete=True)

class EquipmentForm(forms.ModelForm):
    
    class Meta:
        model = Materiel
        fields = ['Mtr_titre', 'Mtr_description']
        
        widgets = {
            'Mtr_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder' : 'Titre'
            }),
            'Mtr_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder' : 'Description'
            })
        }


class StaffForm(forms.ModelForm):

    class Meta:
        model = Personnel
        fields = ['Prs_titre', 'Prs_description']
        
        widgets = {
            'Prs_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder' : 'Titre'
            }),
            'Prs_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder' : 'Description'
            })
        }


class Service2Form(forms.ModelForm):
    
    class Meta:
        model = Prestation2
        fields = ['Ctg_id', 'Ptn2_description', 'Ptn2_delai', 'Ptn2_quantite', 'Ptn2_tarif']
        
        widgets = {
            'Ctg_id': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Ptn2_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Ptn2_delai': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Délai (jrs)'
            }),
            'Ptn2_quantite': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Quantité'
            }),
            'Ptn2_tarif': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Tarif'
            }),
        }
    
    def clean_Ptn2_delai(self):
        Ptn2_delai = self.cleaned_data.get('Ptn2_delai')

        if Ptn2_delai <= 0 :
            raise forms.ValidationError("Le délai souhaité en nombre de jours !")
        
        return Ptn2_delai
    
    def clean_Ptn2_quantite(self):
        Ptn2_quantite = self.cleaned_data.get('Ptn2_quantite')

        if Ptn2_quantite <= 0 :
            raise forms.ValidationError("La quantité ne peut être qu'un entier positif !")
        
        return Ptn2_quantite
    
    def clean_Ptn2_tarif(self):
        Ptn2_tarif = self.cleaned_data.get('Ptn2_tarif')

        if Ptn2_tarif <= 0 :
            raise forms.ValidationError("Le tarif ne peut être qu'un nombre positif !")
        
        return Ptn2_tarif