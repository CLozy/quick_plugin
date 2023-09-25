from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from registration.backends.simple.views import RegistrationView
from multiprocessing import Pool

from .forms import FileUploadForm, SignUpForm, LoginForm


import pandas as pd





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
    return render(request, 'index2.html')

# Create your views here.
def excel_to_qbxml(excel_file):

    # Process the Excel file here, e.g., read and convert Excel to CSV
    excel_df = pd.read_excel(excel_file)  # Read the Excel file into a DataFrame
    excel_df.to_csv(f"quickplugin/fastexcel/data/{excel_file.name[:-4]}.csv", index=False)  # Convert and save as CSV

    #convert csv to qbxml
    
 

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file here, e.g., save it to the server
            uploaded_file = form.cleaned_data['myfile']
            # Perform actions with the uploaded file
            excel_to_qbxml(uploaded_file)


    else:
        form = FileUploadForm()  # Create an instance of the form class

    return render(request, 'index1.html', {'form': form})





