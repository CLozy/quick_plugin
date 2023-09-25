from django import forms
from registration.forms import RegistrationForm 
from django.contrib.auth.forms import AuthenticationForm


class FileUploadForm(forms.Form):
    myfile = forms.FileField(label='Select a file')


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        label='email',
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields['email']
        del self.fields['email']


class SignUpForm(RegistrationForm):
  
    companyname = forms.CharField( label ='Company name', max_length=25, required=True)
    email = forms.EmailField(label ='Your email', max_length=25, required=True)
    password1 = forms.CharField(label ='password', max_length=25, required=True)
    password2 = forms.CharField(label ='Repeat your password', max_length=25, required=True)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.companyname = self.cleaned_data['companyname']

        if commit:
            user.save()

        return user