from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = (
            "owner",
            "slug",
            "created_at",
            "updated_at",
        )
        widgets = {"company_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
           "location": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "established_date": forms.DateInput(attrs={"class": "form-control","type": "date"}),
            "employee_count": forms.NumberInput(attrs={"class": "form-control"}),
        }


