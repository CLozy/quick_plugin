from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from registration.backends.simple.views import RegistrationView
from multiprocessing import Pool

from .forms import FileUploadForm, SignUpForm, LoginForm, ColumnSelectionForm
from formtools.wizard.views import SessionWizardView

from .models import UploadedFile

from .datahandler import excel_to_csv


import pandas as pd
import os

# Create your views here.


#class based views

class MyRegistrationView(RegistrationView):
    # logging.debug("Class initialised")
    template_name = 'registration.html'
    success_url = '/dashboard/'


class MyLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class MyWizard(SessionWizardView):
    form_list = [('file', FileUploadForm), ('columns', ColumnSelectionForm)]
    template_name = 'uploadfile.html'
    file_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'files'))

    def done(self, form_list, form_dict,  **kwargs):
        # Get the uploaded file from the first form
        uploaded_file = form_list[0].cleaned_data
        # Save the uploaded file to the database
        
        uploaded = UploadedFile(file=uploaded_file)
        uploaded.save()

        # Get selected columns from the second form
        selected_columns = form_list[1].cleaned_data
        # Process the uploaded file and selected columns

        return HttpResponseRedirect(reverse('dashboard'))




#function based views
def landing_page(request):
    return render(request, 'index.html')

def dashboard(request): 
    return render(request, 'charts.html')












