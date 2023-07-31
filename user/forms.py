from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from entreprises.models import Entreprise
from user.models import Utilisateur


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label=("Email"), widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "E-mail"}))
    first_name = forms.CharField(max_length=32, required=True, label=("First_name"), widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Prénom(s)"}))
    last_name = forms.CharField(max_length=24, required=True, label=("Last_name"), widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Nom(s)"}))
    password1 = forms.CharField(max_length=32, required=True, strip=False, label=("Password1"), widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Mot de passe"}))
    password2 = forms.CharField(max_length=24, required=True, strip=False, label=("Password2"), widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Confirmation"}))
    Ent_numero_entry = forms.CharField(max_length=16, required=True, label=("Ent_numero"), widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Numéro d'entreprise"}))
    
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'Usr_telephone', 'password1', 'password2', 'Usr_fonction', 'Usr_profil', 'Ent_numero_entry']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nom d\'utilisateur'
            }),
            'Usr_telephone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Téléphone'
            }),
            'Usr_fonction': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Fonction'
            }),
            'Usr_profil': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet e-mail est déjà utilisé.")
        return email
    
    def clean_Ent_numero_entry(self):
        Ent_numero = self.cleaned_data.get('Ent_numero_entry')

        try:
            entreprise = Entreprise.objects.get(Ent_numero=Ent_numero)
            if entreprise == Entreprise.objects.order_by('id').first() :
                raise forms.ValidationError("Veuillez voir l'administrateur pour un telle opération.")

        except Entreprise.DoesNotExist:
            raise forms.ValidationError("L'entreprise avec ce numéro ne s'est pas manifestée.")
        
        return Ent_numero


class SignInForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Nom d\'utilisateur"}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Mot de passe"})
    )


class ChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Ancien mot de passe'
    }), label="New Password")
    new_password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Nouveau mot de passe'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirmation du nouveau'
    }), label="Confirmation")