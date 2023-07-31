from django import forms
from django.forms import formset_factory
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
            raise forms.ValidationError("Le budget ne peut être qu'un entier positif non inférieur à la somme de ceux des étapes !")
        
        return Pjt_budget


class Step1Form(forms.ModelForm):
    def __init__(self, project_form, *args, **kwargs):
        super(Step1Form, self).__init__(*args, **kwargs)
        self.project_form = project_form
    
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
        
    def clean_Etp1_dateDebut(self):
        Etp1_dateDebut = self.cleaned_data.get('Etp1_dateDebut')
        Pjt_dateFin = self.project_form.cleaned_data.get('Pjt_dateFin')

        if Etp1_dateDebut <= Pjt_dateFin:
            raise forms.ValidationError("Respectez les limites du projet !")
        
        return Etp1_dateDebut
    
    def clean_Etp1_dateFin(self):
        Etp1_dateFin = self.cleaned_data.get('Etp1_dateFin')
        Etp1_dateDebut = self.cleaned_data.get('Etp1_dateDebut')
        Pjt_dateFin = self.project_form.cleaned_data.get('Pjt_dateFin')

        if Pjt_dateFin <= Etp1_dateFin or Etp1_dateFin <= Etp1_dateDebut:
            raise forms.ValidationError("Respectez l'ordre des dates et les limites du projet !")
        
        return Etp1_dateFin
    
    def clean_Etp1_budget(self):
        Etp1_budget = self.cleaned_data.get('Etp1_budget')

        if Etp1_budget <= 0 :
            raise forms.ValidationError("Le budget ne peut être qu'un entier positif !")

        return Etp1_budget


Step1FormSet = formset_factory(Step1Form, extra=1, can_delete=True)