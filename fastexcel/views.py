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

STEP_1 = 'file'
STEP_2 = 'columns'
STEP_3 = 'number'

class MyWizard(LoginRequiredMixin, SessionWizardView):
    steps = [STEP_1, STEP_2, STEP_3]
    
    form_list = [(STEP_1, FileUploadForm), (STEP_2, ColumnSelectionForm), (STEP_3, NumberForm)]
    template_name = 'uploadfile.html'
    # Wizard storage
    file_storage = FileSystemStorage(location='wizard/')

   
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == STEP_2:
            # Get the uploaded file from the previous step
            uploaded_file = self.get_cleaned_data_for_step(STEP_1)
            
            if uploaded_file:
                # Extract columns from the uploaded file and pass them to the ColumnSelectionForm
                columns = extract_excel(uploaded_file)  
                # Reinitialize the form with the columns data
                context['wizard']['form'] = ColumnSelectionForm(prefix=STEP_2, columns=columns)
                context['wizard']['text'] = "Please select the columns you want to export" 
                # print(context)
        return context
    
    def get(self, *args, **kwargs):
        # Check if the current step is 'columns'
        if self.steps.current == STEP_2:
            # Get the uploaded file from the previous step
            uploaded_file = self.get_cleaned_data_for_step(STEP_1)
            
            if uploaded_file:
                # Extract columns from the uploaded file and pass them to the ColumnSelectionForm
                columns = extract_excel(uploaded_file)
               
                # Render the 'columns' step with the updated form data
                return self.render(self.get_form(step=STEP_2, data=self.storage.get_step_data(STEP_2)))
        
        # If not at 'columns' step, proceed with the normal flow
        return super().get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        # Check if the current step is 'columns'
        print("Entering post method.")
        # Check if the form is being submitted
        print("Request method:", self.request.method)
        print("Form data:", self.request.POST)
        if self.steps.current == STEP_2:
            import pdb; pdb.set_trace()
            session_data = self.request.session
            print("Session data:", session_data)

            # Get the form instance for the current step
            step_data = self.storage.get_step_data(STEP_2)
            print("Step data:", step_data)
            form = self.get_form(step=STEP_2, data=step_data)

            print("Form instance:", form)

            # Check if the form is valid
            if form.is_valid():
                print("Form is valid. Redirecting to auth_url.")
                # Redirect to 'auth_url' after successful form submission
                auth_url = get_auth_url()
                return HttpResponseRedirect(auth_url)
            else:
                print("Form is not valid:", form.errors)
                # Render the form with errors
                return self.render(form)
                
              
        else:
            print("Not at 'columns' step")

        # If not at 'columns' step or form is not valid, proceed with the normal flow
        return super().post(*args, **kwargs)
    
   
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
  

            #mpesa api at step 3 after redirect from quickbooks callbacks
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











