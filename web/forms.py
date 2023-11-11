# forms.py
from django import forms
from .models import Loans, Users

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loans
        fields = ['dni', 'name_and_last_name', 'genre', 'email', 'requested_amount']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'password']
