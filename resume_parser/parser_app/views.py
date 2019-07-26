import os
import requests
from django.shortcuts import render, redirect
from resume_parser import resume_parser
from .models import UserDetails, Competencies, MeasurableResults, Resume, ResumeDetails, UploadResumeModelForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.authtoken.models import Token
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import UserDetailsSerializer, CompetenciesSerializer, MeasurableResultsSerializer, ResumeSerializer, ResumeDetailsSerializer

def homepage(request):
    if request.method == 'POST':
        user = User.objects.get(id=1)
        UserDetails.objects.filter(user=user).delete()
        Competencies.objects.filter(user=user).delete()
        MeasurableResults.objects.filter(user=user).delete()
        Resume.objects.filter(user=user).delete()
        ResumeDetails.objects.filter(resume__user=user).delete()
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
                    user_details.name           = data.get('name')
                    user_details.email          = data.get('email')
                    user_details.mobile_number  = data.get('mobile_number')
                    user_details.skills         = ', '.join(data.get('skills'))
                    user_details.years_of_exp   = data.get('total_experience')
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
            user_detail = UserDetails.objects.get(user=user)
            messages.success(request, 'Resumes uploaded!')

            overall_score = 0

            competencies = data.get('competencies')
            measurable_results = data.get('measurable_results')

            if competencies and measurable_results:
                overall_score = competencies.get('score') + measurable_results.get('score')
            
            if competencies:
                context = {
                    'resumes': resumes,
                    'competencies': competencies,
                    'measurable_results': measurable_results,
                    'no_of_pages': data.get('no_of_pages'),
                    'total_experience': data.get('total_experience'),
                    'user_details': user_detail,
                    'overall_score': overall_score
                    }
            else:
                context = {
                    'resumes': resumes,
                    'competencies': [],
                    'measurable_results': [],
                    'no_of_pages': data.get('no_of_pages'),
                    'total_experience': data.get('total_experience'),
                    'user_details': user_detail,
                    'overall_score': overall_score
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

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = User.objects.get(pk=pk)
        user_details = UserDetails.objects.get(user=user)
        comp = Competencies.objects.filter(user=user)
        mr = MeasurableResults.objects.filter(user=user)
        resume = Resume.objects.get(user=user)
        resume_details = ResumeDetails.objects.filter(resume=resume)
    except UserDetails.DoesNotExist:
        return HttpResponse(status=404)
    except Competencies.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        comp_serializer = CompetenciesSerializer(comp, many=True)
        mr_serializer = MeasurableResultsSerializer(mr, many=True)
        resume_serializer = ResumeSerializer(resume)
        resume_details_serializer = ResumeDetailsSerializer(resume_details, many=True)
        user_details_serializer = UserDetailsSerializer(user_details)

        data = {}
        data['competencies'] = comp_serializer.data
        data['measurable_results'] = mr_serializer.data
        data['resume'] = resume_serializer.data
        data['resume_details'] = resume_details_serializer.data
        data['user_details'] = user_details_serializer.data
        return JsonResponse(data)

@csrf_exempt
def job_recommendation(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_location = request.POST.get('job_location')
    data = requests.get('https://api.ziprecruiter.com/jobs/v1?search=Python&location=Santa%20Monica&api_key=mqpqz4ev44nfu3n9brazrrix27yzipzm').json()
    return JsonResponse(data)

class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

@api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
@parser_classes([MultiPartParser])
def upload_resume(request):
    request_data            = request.data.dict()
    file_data               = request_data.get('file')
    data                    = eval(request_data.get('signUpDetails'))
    location                = data.get('location')
    desired_job_position    = data.get('desired_job_position')
    designation             = data.get('designation')
    email                   = data.get('email')
    password                = data.get('password1')

    path = default_storage.save(os.path.join(settings.MEDIA_ROOT, file_data.name), ContentFile(file_data.read()))
    parser = resume_parser.ResumeParser(path)
    parsed_data = parser.get_extracted_data()
    try:
        data = {
            'email': email,
            'username': email,
            'password1': password,
            'password2': password,
            }
    except KeyError:
        pass

    response = requests.post("http://localhost:8000/rest-auth/registration/", data=data)
    data = response.json()

    if response.status_code != 400:
        user_id = Token.objects.get(key=data['key']).user_id
        context = {
            'user_id': user_id,
            'token': data['key'],
            'parsed_data': parsed_data
        }
        user = User.objects.get(id=user_id)

        # User Details
        user_details      = UserDetails()
        user_details.user = user
        user_details.name = parsed_data.get('name')
        user_details.email = parsed_data.get('email')
        user_details.skills = parsed_data.get('skills')
        user_details.mobile_number = parsed_data.get('mobile_number')
        user_details.years_of_exp = parsed_data.get('years_of_exp')
        user_details.save()

        # Competencies
        if data.get('competencies'):
            for comp in data.get('competencies'):
                competencies = Competencies()
                competencies.user       = user
                competencies.competency = comp
                competencies.save()

        # Measurable Results
        if data.get('measurable_results'):
            for mr in data.get('measurable_results'):
                measurable_results                   = MeasurableResults()
                measurable_results.user              = user
                measurable_results.measurable_result = mr
                measurable_results.save()

        # Resume
        resume                  = Resume()
        resume.user             = user
        resume.resume           = path
        resume.save()

        # Resume Details
        resume_details          = ResumeDetails()
        resume_details.resume   = resume
        resume_details.page_nos = data.get('no_of_pages')
        resume_details.save()
    else:
        context = data
    return Response(context)