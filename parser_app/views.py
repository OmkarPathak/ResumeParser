from django.shortcuts import render, redirect
from resume_parser import resume_parser
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
import os

def homepage(request):
    if request.method == 'POST':
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()
                    
                    # extracting resume entities
                    parser = resume_parser.ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name          = data.get('name')
                    resume.email         = data.get('email')
                    resume.mobile_number = data.get('mobile_number')
                    # resume.education     = '\n'.join(data.get('education'))
                    resume.education     = get_education(data.get('education'))
                    resume.skills        = ', '.join(data.get('skills'))
                    resume.experience    = ', '.join(data.get('experience'))
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            return render(request, 'base.html', {'resumes': resumes})
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})

def get_education(education):
    '''
    Helper function to display the education in human readable format
    '''
    education_string = ''
    for edu in education:
        education_string += edu[0] + ' (' + str(edu[1]) + '), '
    return education_string.rstrip(', ')