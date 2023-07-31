from datetime import date
from django import forms
from django.forms import formset_factory
from reponses.models import Paiement, Offre, Contrat, Version, Indicateur, Etape2


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Paiement
        fields = ['Pmt_numero', 'Pmt_mode', 'Pmt_description', 'Pmt_montant', 'Pmt_date', 'Pmt_document']

        widgets = {
            'Pmt_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro de paiement'
            }),
            'Pmt_mode': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Mode de paiement'
            }),
            'Pmt_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Pmt_montant': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Montant'
            }),
            'Pmt_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Pmt_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }
    
    def clean_Pmt_montant(self):
        Pmt_montant = self.cleaned_data.get('Pmt_montant')

        if Pmt_montant <= 0 :
            raise forms.ValidationError("Le montant ne peut être qu'un entier positif !")
        
        return Pmt_montant
    
    def clean_Pmt_date(self):
        Pmt_date = self.cleaned_data.get('Pmt_date')

        if date.today() < Pmt_date :
            raise forms.ValidationError("Le futur nous dira lui-même si ce paiement est effectué !")
        
        return Pmt_date


class OfferForm(forms.ModelForm):

    class Meta:
        model = Offre
        fields = ['Ofr_numero', 'Ofr_description', 'Ofr_specifications', 'Ofr_montant', 'Ofr_document']

        widgets = {
            'Ofr_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro d\'offre'
            }),
            'Ofr_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Ofr_specifications': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Spécifications'
            }),
            'Ofr_montant': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Montant'
            }),
            'Ofr_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }
    
    def clean_Ofr_montant(self):
        Ofr_montant = self.cleaned_data.get('Ofr_montant')

        if Ofr_montant <= 0 :
            raise forms.ValidationError("Le montant ne peut être qu'un entier positif !")
        
        return Ofr_montant


class ContractForm(forms.ModelForm):
    Cnt_indicateurs = forms.ModelMultipleChoiceField(
        queryset=Indicateur.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control form-control-lg',
        }))

    class Meta:
        model = Contrat
        fields = ['Cnt_numero', 'Cnt_type', 'Cnt_occurence', 'Cnt_dateDebut', 'Cnt_modeResiliation', 'Cnt_statut', 'Cnt_indicateurs']

        widgets = {
            'Cnt_numero': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Numéro de contrat'
            }),
            'Cnt_type': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Type de contrat'
            }),
            'Cnt_occurence': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'Cnt_dateDebut': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Cnt_modeResiliation': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Mode de résiliation'
            }),
            'Cnt_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }


class VersionForm(forms.ModelForm):
    def __init__(self, contract_form, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.contract_form = contract_form

    class Meta:
        model = Version
        fields = ['Vrs_description', 'Vrs_momentSignature', 'Vrs_dateFin', 'Vrs_document', 'Vrs_modePaiement', 'Vrs_statut']

        widgets = {
            'Vrs_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Vrs_momentSignature': forms.DateTimeInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'datetime-local'
            }),
            'Vrs_dateFin': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Vrs_document': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'Vrs_modePaiement': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Mode de paiement'
            }),
            'Vrs_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
        
    def clean_Vrs_dateFin(self):
        Vrs_dateFin = self.cleaned_data.get('Vrs_dateFin')
        Cnt_dateDebut = self.contract_form.cleaned_data.get('Cnt_dateDebut')

        if Cnt_dateDebut <= Vrs_dateFin:
            raise forms.ValidationError("Respectez les limites du contrat !")
        
        return Vrs_dateFin


class Step2Form(forms.ModelForm):
    def __init__(self, contract_form, *args, **kwargs):
        super(Step2Form, self).__init__(*args, **kwargs)
        self.contract_form = contract_form
    
    class Meta:
        model = Etape2
        fields = ['Etp2_titre', 'Etp2_description', 'Etp2_objectifs', 'Etp2_datePrevue', 'Etp2_dateExecution', 'Etp2_statut']
        
        widgets = {
            'Etp2_titre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Titre'
            }),
            'Etp2_description': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Description'
            }),
            'Etp2_objectifs': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Objectifs'
            }),
            'Etp2_datePrevue': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Etp2_dateExecution': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'Etp2_statut': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            })
        }
        
    def clean_Etp2_datePrevue(self):
        Etp2_datePrevue = self.cleaned_data.get('Etp2_datePrevue')
        Cnt_dateFin = self.contract_form.cleaned_data.get('Cnt_dateFin')

        if Etp2_datePrevue <= Cnt_dateFin:
            raise forms.ValidationError("Respectez les limites du projet !")
        
        return Etp2_datePrevue
    
    def clean_Etp2_dateExecution(self):
        if Etp2_dateExecution:
            Etp2_dateExecution = self.cleaned_data.get('Etp2_dateExecution')
            Etp2_datePrevue = self.cleaned_data.get('Etp2_datePrevue')
            Cnt_dateFin = self.contract_form.cleaned_data.get('Cnt_dateFin')

            if Cnt_dateFin <= Etp2_dateExecution or Etp2_dateExecution <= Etp2_datePrevue:
                raise forms.ValidationError("Respectez l'ordre des dates et les limites du projet !")
        
        return Etp2_dateExecution
    
    def clean_Etp2_budget(self):
        Etp2_budget = self.cleaned_data.get('Etp2_budget')

        if Etp2_budget <= 0 :
            raise forms.ValidationError("Le budget ne peut être qu'un entier positif !")

        return Etp2_budget


Step2FormSet = formset_factory(Step2Form, extra=1, can_delete=True)


class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicateur
        fields = ['Ind_intitule', 'Ind_ponderation']

        widgets = {
            'Ind_intitule': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Intitulé'
            }),
            'Ind_ponderation': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Coefficient'
            }),
        }
    
    def clean_Ind_ponderation(self):
        Ind_ponderation = self.cleaned_data.get('Ind_ponderation')

        if Ind_ponderation <= 0 :
            raise forms.ValidationError("Le coefficient ne peut être qu'un entier positif !")
        
        return Ind_ponderation