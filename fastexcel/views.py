from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from registration.backends.simple.views import RegistrationView
from multiprocessing import Pool

from .forms import FileUploadForm, SignUpForm, LoginForm

from .datahandler import excel_to_csv

import pandas as pd

# Create your views here.

class MyRegistrationView(RegistrationView):
    # logging.debug("Class initialised")
    template_name = 'registration.html'
    success_url = '/dashboard/'


class MyLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm



def landing_page(request):
    return render(request, 'index.html')

def dashboard(request): 
    return render(request, 'charts.html')




def upload_file(request):
    if request.method == 'POST':
        
        form = FileUploadForm(request.POST, request.FILES)
        error_message = None
        if form.is_valid():
            # Handle the uploaded file here, e.g., save it to the server
            uploaded_file = form.cleaned_data['file']
            try:
                uploaded_file = form.cleaned_data['file']
                print(uploaded_file)
                # Try to read the file as an Excel file
                excel_to_csv(uploaded_file)  

                # Perform actions with the Excel data
            except Exception as file_e:
                # If it's not an Excel file, handle the error
                error_message = "The uploaded file is not a valid Excel file."      

    else:
        form = FileUploadForm()  # Create an instance of the form class

    # form.add_error(None, error_message)

    return render(request, 'uploadfile.html', {'form': form, 'error_message': error_message})




