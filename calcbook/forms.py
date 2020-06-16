from django.forms import ModelForm , TextInput , CheckboxInput
from django.utils.translation import gettext_lazy as _
from . models import Services , Customers

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
                'class':'form-check-input',
            }),
            'paid_amt': TextInput(attrs={
                'class':'form-control shadow-none',
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