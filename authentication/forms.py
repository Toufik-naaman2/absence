from django import forms
from config.models import Class  # Import Class from your gestion_absence app

from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']  # Only name field for now




class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'role',
            'password1',
            'password2',
        ]
