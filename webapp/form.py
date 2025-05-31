# forms.py
from django import forms
from .models import Donor

class SupportIntentForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone', 'country', 'amount', 'message', 'anonimity']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
