from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm

# Create your views here.

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file here, e.g., save it to the server
            uploaded_file = form.cleaned_data['myfile']
            # Perform actions with the uploaded file

            # You can save the file to a specific location if needed
            # uploaded_file.name will give you the original filename
            uploaded_file.save('quickplugin/fastexcel/data' + uploaded_file.name)
            

            # You can also access the file's content using uploaded_file.read()

    else:
        form = FileUploadForm()  # Create an instance of the form class

    return render(request, 'index.html', {'form': form})



def excel_to_qbxml(excel_file):
    pass