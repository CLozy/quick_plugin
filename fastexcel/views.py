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

from .datahandler import  extract_excel


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


    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'columns':
            # Get the uploaded file from the previous step
            uploaded_file = self.get_cleaned_data_for_step('file')
            
            if uploaded_file:
                # Extract columns from the uploaded file and pass them to the ColumnSelectionForm
                columns = extract_excel(uploaded_file)  # Replace with your logic  
                # Reinitialize the form with the columns data
                context['wizard']['form'] = ColumnSelectionForm(prefix='columns', columns=columns)
                context['wizard']['text'] = "Please select the columns you want to export" 
                print(context)
        return context
    
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












