
from django import forms
from .models import Employee, ServiceRecord

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "first_name", "last_name", "personnel_code", "national_code",
            "age", "service_years", "service_months", "rank", "status",
            "unit", "position", "phone", "notes"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": ""}),
            "last_name": forms.TextInput(attrs={"placeholder": ""}),
            "personnel_code": forms.TextInput(attrs={"placeholder": ""}),
            "national_code": forms.TextInput(attrs={"placeholder": ""}),
            "age": forms.NumberInput(attrs={"min": 18, "max": 100}),
            "service_years": forms.NumberInput(attrs={"min": 0, "max": 60}),
            "service_months": forms.NumberInput(attrs={"min": 0, "max": 11}),
            "unit": forms.TextInput(attrs={"placeholder": ""}),
            "position": forms.TextInput(attrs={"placeholder": ""}),
            "phone": forms.TextInput(attrs={"placeholder": ""}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_service_months(self):
        value = self.cleaned_data["service_months"]
        if value > 11:
            raise forms.ValidationError("تعداد ماه باید بین ۰ تا ۱۱ باشد.")
        return value


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ["title", "from_date", "to_date", "description"]
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class RegisterForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=150)
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        if data.get("password1") != data.get("password2"):
            raise forms.ValidationError("رمزهای عبور یکسان نیستند.")
        return data
