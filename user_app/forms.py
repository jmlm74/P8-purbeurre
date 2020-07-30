from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserPurBeurreForm(forms.ModelForm):
    """
    User connection/creation form

    from User model with email field
    password confirmation (used only for creation)

    clean data method:
        username is the left part of mail address (before @)
        if user creation :
                Validate password and confirm password match (if no
                raise Validation error with message)
                Validate username does not exist (if yes raise Validation error with message)
    """
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(
                                       attrs={'placeholder': 'Seulement pour création'}
                                       ),
                                       required=False,
                                       label="Confirmation",
                                       )
    connexion_creation = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super(UserPurBeurreForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("email").split("@")[0]
        connex_creation = cleaned_data.get("connexion_creation")

        if connex_creation != "connexion":  # connection --> no password special validation
            if password != confirm_password:  # passwords don't match
                raise forms.ValidationError(
                    "Mot de passe et confirmation ne correspondent pas !"
                )
            try:
                validate_password(password)  # password validation for user-creation
            except forms.ValidationError as err:
                raise forms.ValidationError(err)
            try:
                User.objects.get(username=username)  # user already exists ?
            except User.DoesNotExist:
                pass  # user does not exist --> OK
            else:
                raise forms.ValidationError(f"Erreur : Utilisateur {username} déjà créé ! ")
