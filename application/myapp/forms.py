from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationFrom(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput
    (attrs={'autofocus' : 'True', 'class': 'from-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput
    (attrs={'class' : 'from-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput
    (attrs={'class' : 'from-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'from-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }

        