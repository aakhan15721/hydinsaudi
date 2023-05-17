from django import forms

class ExpatadFilterForm(forms.Form):
    fullname = forms.CharField()

