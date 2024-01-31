from django import forms
from projets.models import Projet_d_Approvisionnement, Etape1


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Projet_d_Approvisionnement
        fields = ['Pjt_numero', 'Pjt_titre', 'Pjt_description', 'Pjt_dateDebut', 'Pjt_dateFin', 'Pjt_objectifs', 'Pjt_document', 'Pjt_budget', 'Pjt_statut']

        widgets = {
            'Pjt_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro de Projet'
            }),
            'Pjt_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Pjt_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Pjt_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Pjt_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Pjt_objectifs': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Objectifs'
            }),
            'Pjt_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Pjt_budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Budget'
            }),
            'Pjt_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
    
    def clean_Pjt_dateFin(self):
        Pjt_dateDebut = self.cleaned_data.get('Pjt_dateDebut')
        Pjt_dateFin = self.cleaned_data.get('Pjt_dateFin')

        if Pjt_dateFin <= Pjt_dateDebut :
            raise forms.ValidationError("Respectez l'ordre des dates !")
        
        return Pjt_dateFin
    
    def clean_Pjt_budget(self):
        Pjt_budget = self.cleaned_data.get('Pjt_budget')

        if Pjt_budget <= 0:
            raise forms.ValidationError("Le budget ne peut être qu'un nombre positif non inférieur à la somme de ceux des étapes !")
        
        return Pjt_budget


class Step1Form(forms.ModelForm):
    
    class Meta:
        model = Etape1
        fields = ['Etp1_titre', 'Etp1_description', 'Etp1_objectifs', 'Etp1_dateDebut', 'Etp1_dateFin',  'Etp1_budget', 'Etp1_statut']
        
        widgets = {
            'Etp1_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Etp1_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Etp1_objectifs': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Objectifs'
            }),
            'Etp1_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Etp1_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Etp1_budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Budget'
            }),
            'Etp1_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
    
    def clean_Etp1_budget(self):
        Etp1_budget = self.cleaned_data.get('Etp1_budget')

        if Etp1_budget <= 0 :
            raise forms.ValidationError("Le budget ne peut être qu'un nombre positif !")

        return Etp1_budget