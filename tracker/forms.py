from django import forms
from .models import SupplementRecord

class SupplementRecordForm(forms.ModelForm):
    class Meta:
        model = SupplementRecord
        fields = ['supplement_name', 'intake_datetime', 'amount']
