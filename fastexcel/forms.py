from django import forms

class FileUploadForm(forms.Form):
    myfile = forms.FileField(label='Select a file')
