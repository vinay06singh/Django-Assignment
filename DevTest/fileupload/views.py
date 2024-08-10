from django.shortcuts import render, redirect
from .forms import FileUploadForm
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

def send_summary_email(summary, recipients):
    send_mail(
        subject='Python Assignment - Vinay Singh',
        message='',
        html_message=summary,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients
    )

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            file_path = file.file.path  
            df = pd.read_excel(file_path)  

            
            extracted_data = df[['Cust State', 'Cust Pin', 'DPD']]
            
            try:
                extracted_data = df[['Cust State', 'Cust Pin', 'DPD']]
            except KeyError as e:
                return render(request, 'fileupload/upload.html', {
                    'form': form,
                    'error': f"Missing columns: {e}"
                })

            summary = extracted_data.to_html(index=False)

            send_summary_email(summary, ['vinay264singh@gmail.com'])

            return render(request, 'fileupload/summary.html', {'summary': summary})
    else:
        form = FileUploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})






