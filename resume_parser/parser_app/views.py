from django.shortcuts import render, redirect
from .ai_service import get_resume_insights
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, FileResponse, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from .utils import extract_text

def homepage(request):
    if request.method == 'POST':
        # Removed Resume.objects.all().delete() to maintain history
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.is_ajax()

        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.tag = request.POST.get('tag') # Save the tag
                    resume.save()
                    
                    # New Logic: Extract Text -> AI Analysis
                    file_path = os.path.join(settings.MEDIA_ROOT, resume.resume.name)
                    ext = os.path.splitext(file_path)[1]
                    
                    resume_text = extract_text(file_path, ext)
                    data = get_resume_insights(resume_text)
                    
                    if data:
                        resume.name           = data.get('name')
                        resume.email          = data.get('email')
                        resume.mobile_number  = data.get('mobile_number')
                        # Ensure education and skills are stored as strings if they come as lists
                        resume.education      = ', '.join(data.get('education')) if isinstance(data.get('education'), list) else data.get('education')
                        resume.skills         = ', '.join(data.get('skills')) if isinstance(data.get('skills'), list) else data.get('skills')
                        resume.company_names  = ', '.join(data.get('company_names')) if isinstance(data.get('company_names'), list) else data.get('company_names')
                        resume.college_name   = data.get('college_name')
                        resume.designation    = data.get('designation')
                        resume.total_experience = data.get('total_experience')
                        resume.experience     = ', '.join(data.get('experience')) if isinstance(data.get('experience'), list) else data.get('experience')
                        resume.ai_summary     = data.get('ai_summary')
                        resume.ai_strengths   = data.get('ai_strengths')

                    resume.save() # Save again after populating extracted data
                except IntegrityError:
                    if is_ajax:
                        return JsonResponse({'status': 'error', 'message': f'Duplicate resume found: {file.name}'}, status=400)
                    messages.warning(request, f'Duplicate resume found: {file.name}')
                    return redirect('homepage')
                except Exception as e:
                    print(f"Error during resume parsing for {file.name}: {e}")
                    if is_ajax:
                        return JsonResponse({'status': 'error', 'message': f'Error processing {file.name}: {e}'}, status=500)
                    messages.error(request, f'Error processing {file.name}: {e}')
                    # Optionally, you might want to delete the partially saved resume here
                    # resume.delete()
                    return redirect('homepage')
            
            if is_ajax:
                return JsonResponse({'status': 'success', 'message': 'File uploaded successfully'})

            messages.success(request, 'Resumes uploaded!')

            return redirect('resumes_list')
    else:
        form = UploadResumeModelForm()
    return render(request, 'home.html', {'form': form})

def resumes_list(request):
    resumes = Resume.objects.all().order_by('-uploaded_on')
    
    # Get distinct tags for filter dropdown
    tags = Resume.objects.exclude(tag__isnull=True).exclude(tag__exact='').values_list('tag', flat=True).distinct()
    
    # Filter by tag
    selected_tag = request.GET.get('tag')
    if selected_tag:
        resumes = resumes.filter(tag=selected_tag)
    
    # Search by keyword
    search_query = request.GET.get('q')
    if search_query:
        resumes = resumes.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(skills__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(education__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(resumes, 10) # Show 10 resumes per page
    page_number = request.GET.get('page')
    try:
        resumes = paginator.page(page_number)
    except PageNotAnInteger:
        resumes = paginator.page(1)
    except EmptyPage:
        resumes = paginator.page(paginator.num_pages)

    context = {
        'resumes': resumes,
        'tags': tags,
        'selected_tag': selected_tag,
        'search_query': search_query,
    }
    return render(request, 'resumes_list.html', context)

def delete_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    resume.delete()
    messages.success(request, 'Resume deleted successfully!')
    return redirect('resumes_list')

def update_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    if request.method == 'POST':
        resume.name = request.POST.get('name')
        resume.email = request.POST.get('email')
        resume.mobile_number = request.POST.get('mobile_number')
        resume.tag = request.POST.get('tag')
        resume.designation = request.POST.get('designation')
        resume.college_name = request.POST.get('college_name')
        resume.education = request.POST.get('education')
        resume.skills = request.POST.get('skills')
        resume.experience = request.POST.get('experience')
        resume.ai_summary = request.POST.get('ai_summary')
        resume.ai_strengths = request.POST.get('ai_strengths')
        resume.remark = request.POST.get('remark')
        resume.save()
        messages.success(request, 'Resume details updated successfully!')
        return redirect('resumes_list')
    return render(request, 'update_resume.html', {'resume': resume})

import csv
def export_resumes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resumes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Mobile Number', 'Tag', 'Education', 'Skills', 'Company Names', 'Designation', 'Experience', 'Uploaded On'])

    resumes = Resume.objects.all().order_by('-uploaded_on')

    # Filter by tag
    selected_tag = request.GET.get('tag')
    if selected_tag:
        resumes = resumes.filter(tag=selected_tag)

    # Search by keyword
    search_query = request.GET.get('q')
    if search_query:
        resumes = resumes.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(skills__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(education__icontains=search_query)
        )

    resumes_values = resumes.values_list('name', 'email', 'mobile_number', 'tag', 'education', 'skills', 'company_name', 'designation', 'experience', 'uploaded_on')

    for resume in resumes_values:
        writer.writerow(resume)

    return response