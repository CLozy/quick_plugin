from django import forms
from registration.forms import RegistrationForm


class FileUploadForm(forms.Form):
    myfile = forms.FileField(label='Select a file')


class LoginForm(forms.Form):
    email = forms.EmailField(label ='email', max_length=25, required=True)
    password = forms.CharField(label ='password', max_length=25, required=True)


class SignUpForm(RegistrationForm):
  
    username = forms.CharField( label ='Company name', max_length=25, required=True )
    email = forms.EmailField(label ='Your email', max_length=25, required=True)
    password1 = forms.CharField(label ='password', max_length=25, required=True)
    password2 = forms.CharField(label ='Repeat your password', max_length=25, required=True)
