from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from registration.backends.simple.views import RegistrationView
from multiprocessing import Pool

from .forms import FileUploadForm, SignUpForm, LoginForm

from .datahandler import excel_to_csv



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
        if form.is_valid():
            # Handle the uploaded file here, e.g., save it to the server
            uploaded_file = form.cleaned_data['file']
            # Perform actions with the uploaded file
            excel_to_csv(uploaded_file)
            


    else:
        form = FileUploadForm()  # Create an instance of the form class

    return render(request, 'uploadfile.html', {'form': form})




