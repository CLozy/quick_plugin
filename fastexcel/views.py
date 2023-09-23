from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm
import pandas as pd
from multiprocessing import Pool

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


def landing_page(request):
    return render(request, 'index.html')



    # return qbxml_file