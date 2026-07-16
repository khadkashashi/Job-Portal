from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("first_name","last_name", "location","resume", "cover_letter")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "cover_letter": forms.Textarea(attrs={"class": "form-control","rows": 6,"placeholder": "Tell the recruiter why you're a good fit."}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }