from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class ShippingAdressForm(forms.Form):
    street_adress=forms.CharField(widget=forms.TextInput(attrs={
    'class':'form-control' ,
    'id':'floatingInput',
    'placeholder':'Street and house number',
    }))
    appartment_adress=forms.CharField(widget=forms.TextInput(attrs={
    'class':'form-control' ,
    'id':'floatingApartment',
    'placeholder':'Apartement',
    }))
    country=CountryField(blank_label='select country').formfield(widget=CountrySelectWidget(attrs={
    'class':'form-control' ,
    'id':'floatingSelect',
    'placeholder':'Select country',
    'aria-label':'Select country',
    }))
    zip_code=forms.CharField(widget=forms.TextInput(attrs={
    'class':'form-control' ,
    'id':'floatingZip',
    'placeholder':'Zip code',
    }))


class CouponForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Coupon code',
    }))








