from django import forms
from registration.forms import RegistrationForm 
from django.contrib.auth.forms import AuthenticationForm




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
    
class FileUploadForm(forms.Form):
    file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            if not uploaded_file.name.lower().endswith(('.xls', '.xlsx')):
                raise forms.ValidationError("The uploaded file is not a valid Excel file.")
        return uploaded_file



class ColumnSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns', [])
        super(ColumnSelectionForm, self).__init__(*args, **kwargs)

        for column in columns:
            self.fields[column] = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check form-check-my-class' , 'id': 'checkLabel'}))


class NumberForm(forms.Form):
    number_input = forms.IntegerField(label='Enter a Number')