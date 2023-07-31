from django import forms
from appels.models import Appel_a_Manifestation, Appel_d_Offre, Prestation1, Critere
from entreprises.models import Categorie


class CallManifestForm(forms.ModelForm):
    
    class Meta:
        model = Appel_a_Manifestation
        fields = ['Ami_numero', 'Ami_titre', 'Ami_description', 'Ami_dateDebut', 'Ami_dateFin', 'Ami_delaiValidite', 'Ami_document', 'Ami_coordonnees', 'Ami_statut']
        
        widgets = {
            'Ami_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro d\'appel'
            }),
            'Ami_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Ami_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Ami_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Ami_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Ami_delaiValidite': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Délai de validité (jrs)'
            }),
            'Ami_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Ami_coordonnees': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Coordonnées'
            }),
            'Ami_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
    
    def clean_Ami_dateFin(self):
        Ami_dateDebut = self.cleaned_data.get('Ami_dateDebut')
        Ami_dateFin = self.cleaned_data.get('Ami_dateFin')

        if Ami_dateFin <= Ami_dateDebut :
            raise forms.ValidationError("Respectez l'ordre des dates !")
        
        return Ami_dateFin
    
    def clean_Ami_delaiValidite(self):
        Ami_delaiValidite = self.cleaned_data.get('Ami_delaiValidite')

        if Ami_delaiValidite <= 0 :
            raise forms.ValidationError("La durée du projet en nombre de jours !")
        
        return Ami_delaiValidite


class CallOfferForm(forms.ModelForm):
    Apl_prestations = forms.ModelMultipleChoiceField(
        queryset=Prestation1.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control form-control-lg',
        }))
    Apl_criteres = forms.ModelMultipleChoiceField(
        queryset=Critere.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control form-control-lg',
        }))


    class Meta:
        model = Appel_d_Offre
        fields = ['Apl_numero', 'Apl_titre', 'Apl_description', 'Apl_exigences', 'Apl_dateDebut', 'Apl_dateFin', 'Apl_document', 'Apl_coordonnees', 'Apl_budget', 'Apl_statut', 'Apl_prestations', 'Apl_criteres']

        widgets = {
            'Apl_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro d\'appel'
            }),
            'Apl_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Apl_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Apl_exigences': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Exigences'
            }),
            'Apl_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Apl_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Apl_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Apl_coordonnees': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Coordonnées'
            }),
            'Apl_budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Budget'
            }),
            'Apl_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
    
    def clean_Apl_dateFin(self):
        Apl_dateDebut = self.cleaned_data.get('Apl_dateDebut')
        Apl_dateFin = self.cleaned_data.get('Apl_dateFin')

        if Apl_dateFin <= Apl_dateDebut :
            raise forms.ValidationError("Respectez l'ordre des dates !")
        
        return Apl_dateFin
    
    def clean_Apl_budget(self):
        Apl_budget = self.cleaned_data.get('Apl_budget')

        if Apl_budget <= 0 :
            raise forms.ValidationError("Le budget ne peut être qu'un entier positif !")
        
        return Apl_budget


class Service1Form(forms.ModelForm):
    
    class Meta:
        model = Prestation1
        fields = ['Ctg_id', 'Ptn1_description', 'Ptn1_delai', 'Ptn1_quantite', 'Ptn1_budget']
        
        widgets = {
            'Ctg_id': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Ptn1_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Ptn1_delai': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Délai (jrs)'
            }),
            'Ptn1_quantite': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Quantité'
            }),
            'Ptn1_budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Budget'
            }),
        }
    
    def clean_Ptn1_delai(self):
        Ptn1_delai = self.cleaned_data.get('Ptn1_delai')

        if Ptn1_delai <= 0 :
            raise forms.ValidationError("Le délai souhaité en nombre de jours !")
        
        return Ptn1_delai
    
    def clean_Ptn1_quantite(self):
        Ptn1_quantite = self.cleaned_data.get('Ptn1_quantite')

        if Ptn1_quantite <= 0 :
            raise forms.ValidationError("La quantité ne peut être qu'un entier positif !")
        
        return Ptn1_quantite
    
    def clean_Ptn1_budget(self):
        Ptn1_budget = self.cleaned_data.get('Ptn1_budget')

        if Ptn1_budget <= 0 :
            raise forms.ValidationError("Le budget ne peut être qu'un entier positif !")
        
        return Ptn1_budget


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Categorie
        fields = ['Ctg_titre']
        
        widgets = {
            'Ctg_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder' : 'Titre'
            })
        }


class CriteriaForm(forms.ModelForm):
    
    class Meta:
        model = Critere
        fields = ['Crt_intitule', 'Crt_ponderation']
        
        widgets = {
            'Crt_intitule': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Intitulé'
            }),
            'Crt_ponderation': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Coefficient'
            })
        }
    
    def clean_Crt_ponderation(self):
        Crt_ponderation = self.cleaned_data.get('Crt_ponderation')

        if Crt_ponderation <= 0 :
            raise forms.ValidationError("Le coefficient ne peut être qu'un entier positif !")
        
        return Crt_ponderation