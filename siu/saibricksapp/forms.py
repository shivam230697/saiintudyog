from django import forms
from .models import AccountModel


class AccountForm(forms.ModelForm):
    class Meta:
        model = AccountModel
        fields = '__all__'

