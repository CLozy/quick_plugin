from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from registration.backends.simple.views import RegistrationView
from multiprocessing import Pool
from formtools.wizard.views import SessionWizardView



from .forms import FileUploadForm, SignUpForm, LoginForm, ColumnSelectionForm, NumberForm
from .models import UploadedFile

from .datahandler import  extract_excel , get_column_data

from .qb import get_auth_url, get_access_token

from .pay import MpesaPay

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


class MyWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [('file', FileUploadForm), ('columns', ColumnSelectionForm), ('number', NumberForm)]
    template_name = 'uploadfile.html'
    # Wizard storage
    file_storage = FileSystemStorage(location='wizard/')

   
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'columns':
            # Get the uploaded file from the previous step
            uploaded_file = self.get_cleaned_data_for_step('file')
            
            if uploaded_file:
                # Extract columns from the uploaded file and pass them to the ColumnSelectionForm
                columns = extract_excel(uploaded_file)  
                # Reinitialize the form with the columns data
                context['wizard']['form'] = ColumnSelectionForm(prefix='columns', columns=columns)
                context['wizard']['text'] = "Please select the columns you want to export" 
                # print(context)
        return context
    
   
    def done(self, form_list, form_dict,  **kwargs):
        # Get the uploaded file from the first form
        uploaded_file_data = form_list[0].cleaned_data.get('file')  # Assuming 'file' is the field name in your FileUploadForm

        if uploaded_file_data:
           
            user = self.request.user
            uploaded_file = UploadedFile(user=user, file=uploaded_file_data)
            # uploaded_file.file = uploaded_file_data  # Assign the uploaded file directly
            uploaded_file.save()

                      
            # Convert the generator into a list
            column_form_data = list(form_list[1].data.items())
            
            # Extract selected columns
            selected_columns = [key.split('-')[1] for key, value in column_form_data if value == 'on']
        

            # Process the uploaded file and selected columns
            columns_data = get_column_data(uploaded_file_data, selected_columns)

            
            # QuickBooks authentication URL at step 2
            if self.steps.current == 'columns':
                auth_url = get_auth_url()
                return HttpResponseRedirect(auth_url)

            #mpesa pay api at step 3 after redirect from quickbooks callbacks
            # payment = MpesaPay().stk_push(shortcode=None)

        return HttpResponseRedirect('dashboard')



#Quickbook callback 
class QuickBooksCallbackView(View):
    def get(self, request):
        # Handle the callback from QuickBooks
        authorization_code = request.GET.get('code')
        if authorization_code:
            # Authorization code is present, proceed with getting access token
            get_access_token(authorization_code)
            # Redirect back to the next step 3 of the wizard
            return redirect(reverse('upload', args=['number'])) 
            



#function based views
def landing_page(request):
    return render(request, 'index.html')


def dashboard(request): 
    #get the tottal number of uploaded files from the fastexcel_uploadfile db table based on the user of the request
    user = request.user
    total_files = UploadedFile.objects.filter(user=user).count()
    return render(request, 'charts.html' , {'total_files':total_files})











