from django import forms
from application.models import  CustomerRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ['customer_name', 'phone', 'medicine_details']
        widgets = {
            'medicine_details': forms.Textarea(attrs={'rows': 3}),
            'phone': forms.TextInput(attrs={'maxlength': 10}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
