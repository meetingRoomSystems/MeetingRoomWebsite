from django import forms

class GetLogin(forms.Form):
    username = forms.CharField(max_length = 100,required = True)
    password = forms.CharField(max_length = 100,required = True)

class GetRegister(forms.Form):
    fullname = forms.CharField(max_length = 100,required = True)
    username = forms.CharField(max_length = 100,required = True)
    password = forms.CharField(max_length = 100,required = True)
