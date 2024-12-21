from django import forms
from django.contrib.auth.forms import UserCreationForm
from custom_user.models import User  # Adjust the import to your custom user model

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field_reg'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field_reg'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input-field_reg'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field_reg'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field_reg'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        email = self.cleaned_data['email']
        user.email = email 
        if commit:
            user.save()
        return user

