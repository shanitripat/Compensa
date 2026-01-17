from django import forms
from .models import PayrollSubmission, PayrollEntry

class PayrollSubmissionForm(forms.ModelForm):
    class Meta:
        model = PayrollSubmission
        fields = ['payroll_month']
        widgets = {'payroll_month': forms.TextInput(attrs={'placeholder': "e.g., Dec'25"})}

class PayrollEntryForm(forms.ModelForm):
    class Meta:
        model = PayrollEntry
        exclude = ['submission']
        widgets = {'remarks': forms.Textarea(attrs={'rows':2})}