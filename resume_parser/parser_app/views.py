from django.shortcuts import render, redirect
from resume_parser import resume_parser
from .models import UserDetails, Competencies, MeasurableResults, Resume, ResumeDetails, UploadResumeModelForm
from django.contrib.auth.models import User
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
        if file_form.is_valid():
            for file in files:
                try:
                    user = User.objects.get(id=1)

                    # saving the file
                    resume = Resume(user=user, resume=file)
                    resume.save()
                    
                    # extracting resume entities
                    parser = resume_parser.ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    
                    # User Details
                    # resume.name          = data.get('name')
                    # resume.email         = data.get('email')
                    # resume.education     = get_education(data.get('education'))
                    user_details = UserDetails()
                    user_details.user           = user
                    user_details.mobile_number = data.get('mobile_number')
                    user_details.skills        = ', '.join(data.get('skills'))
                    user_details.years_of_exp  = data.get('total_experience')
                    user_details.save()

                    for comp in data.get('competencies'):
                        competencies = Competencies()
                        competencies.user       = user
                        competencies.competency = comp
                        competencies.save()

                    for mr in data.get('measurable_results'):
                        measurable_results                   = MeasurableResults()
                        measurable_results.user              = user
                        measurable_results.measurable_result = mr
                        measurable_results.save()

                    # Resume Details
                    resume_details          = ResumeDetails()
                    resume_details.resume   = resume
                    resume_details.page_nos = data.get('no_of_pages')
                    resume_details.save()

                    # resume.experience    = ', '.join(data.get('experience'))
                    # measurable_results.append(data.get('measurable_results'))
                    # resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')

            resumes = Resume.objects.filter(user=User.objects.get(id=1))
            messages.success(request, 'Resumes uploaded!')
            
            competencies = []
            measurable_results = []
            
            competencies.append(data.get('competencies'))
            measurable_results.append(data.get('measurable_results'))
            
            if competencies:
                context = {
                    'resumes': resumes,
                    'competencies': competencies,
                    'measurable_results': measurable_results,
                    'no_of_pages': data.get('no_of_pages'),
                    'total_experience': data.get('total_experience'),
                    }
            else:
                context = {
                    'resumes': resumes,
                    'competencies': [],
                    'measurable_results': []
                    }
            return render(request, 'base.html', context)
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