from django import forms
from .models import Application
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ( "resume", "cover_letter", )
        widgets = { "cover_letter": forms.Textarea(  attrs={  "class": "form-control","rows": 6,"placeholder": "Tell the recruiter why you're a good fit."  } ),
        "resume": forms.ClearableFileInput( attrs={   "class": "form-control"} ), }