from django import forms
from django.utils import timezone

from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ( "company", "slug", "created_at","updated_at" )
        widgets = { "title": forms.TextInput( attrs={ "class": "form-control", "placeholder": "Python Backend Developer"}),
            "description": forms.Textarea(attrs={ "class": "form-control","rows": 6, "placeholder": "Describe the role..."}),
            "location": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Kathmandu"}),
            "employment_type": forms.Select(attrs={"class": "form-select"}),
            "experience_level": forms.Select( attrs={"class": "form-select"}),
            "salary_min": forms.NumberInput(attrs={"class": "form-control","placeholder": "50000" }),
            "salary_max": forms.NumberInput( attrs={"class": "form-control","placeholder": "80000"}),
            "vacancies": forms.NumberInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"})}

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get("salary_min")
        salary_max = cleaned_data.get("salary_max")
        deadline = cleaned_data.get("deadline")
        if salary_min and salary_max:
            if salary_min > salary_max:
                raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        if deadline:
            if deadline < timezone.now().date():
                raise forms.ValidationError("Deadline cannot be in the past.")
        return cleaned_data