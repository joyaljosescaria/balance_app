from django import forms
from django.forms import ModelForm , TextInput , CheckboxInput
from django.utils.translation import gettext_lazy as _
from . models import Services , Customers , Amount_debit

class ServicesForm(ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'service_name': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'customer_id': TextInput(attrs={
                'class':'form-control',
                'type': 'hidden'
            }),
            'service_charge': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'profit': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'isPaid': CheckboxInput(attrs={
                'class':'ios8-switch',
                'id': 'checkbox-1',
            }),
            'paid_amt': TextInput(attrs={
                'class':'form-control shadow-none',
            }), 
            'service_date': TextInput(attrs={
                'class':'form-control shadow-none',
                'type': 'hidden'
            }),
            'bal_paid_date': TextInput(attrs={
                'class':'form-control datepicker ',
                'data-date-format':'mm/dd/yyyy'
            }),
        }

class CustomerAddForm(ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'phone': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'email': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
        }

class DebitForm(ModelForm):
    class Meta:
        model = Amount_debit
        fields = '__all__'
        widgets = {
            'debit_use': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
            'debit_amt': TextInput(attrs={
                'class':'form-control shadow-none',
            }),
        }

class DateForm(forms.Form):
    date1 = forms.CharField(max_length=15 ,widget=forms.TextInput(attrs={
        'class': 'form-control shadow-none',
        'id' : 'date-1'
    }))
    date2 = forms.CharField(max_length=15 ,widget=forms.TextInput(attrs={
        'class': 'form-control shadow-none',
        'id' : 'date-2'
    })) 
    