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

from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import connection
from django.db.models import Avg
import time

def process_single_resume(file, tag):
    """
    Worker function to process a single resume in a separate thread.
    """
    start_time = time.time()
    try:
        # Re-fetch resume to ensure freshness
        resume = Resume.objects.get(id=file) # 'file' argument here being the ID
        
        file_path = os.path.join(settings.MEDIA_ROOT, resume.resume.name)
        ext = os.path.splitext(file_path)[1]
        
        # 1. Text Extraction (I/O Bound)
        resume_text = extract_text(file_path, ext)
        
        # 2. AI Analysis (Compute/Network Bound)
        data = get_resume_insights(resume_text)
        
        if data:
            resume.name           = data.get('name')
            resume.email          = data.get('email')
            resume.mobile_number  = data.get('mobile_number')
            resume.education      = ', '.join(data.get('education')) if isinstance(data.get('education'), list) else data.get('education')
            resume.skills         = ', '.join(data.get('skills')) if isinstance(data.get('skills'), list) else data.get('skills')
            resume.company_names  = ', '.join(data.get('company_names')) if isinstance(data.get('company_names'), list) else data.get('company_names')
            resume.college_name   = data.get('college_name')
            resume.designation    = data.get('designation')
            resume.total_experience = data.get('total_experience')
            resume.experience     = ', '.join(data.get('experience')) if isinstance(data.get('experience'), list) else data.get('experience')
            resume.ai_summary     = data.get('ai_summary')
            resume.ai_strengths   = data.get('ai_strengths')
            
            # Calculate processing time
            end_time = time.time()
            resume.processing_time = round(end_time - start_time, 2)
            
            resume.save()

            # 3. Auto-Index into Vector Store (New)
            try:
                from .agents.vector_store import VectorStore
                vector_store = VectorStore()
                text = f"{resume.skills or ''} {resume.experience or ''} {resume.ai_summary or ''}"
                metadata = {
                    'id': resume.id,
                    'name': resume.name,
                    'email': resume.email,
                    'skills': resume.skills,
                    'ai_summary': resume.ai_summary,
                    'file_url': resume.resume.url if resume.resume else ''
                }
                vector_store.add_document(text, metadata)
                print(f"Auto-Indexed: {resume.name}")
            except Exception as vs_e:
                print(f"Vector Store Error: {vs_e}")

            return f"Success: {resume.resume.name}"
            
    except Exception as e:
        print(f"Worker Error for {file}: {e}")
        return f"Error: {e}"
    finally:
        # Close connection to prevent leaks in threads
        connection.close()

def jd_matcher(request):
    """
    View to match Job Description against indexed resumes.
    """
    if request.method == 'POST':
        job_description = request.POST.get('job_description')
        if job_description:
            try:
                from .agents.vector_store import VectorStore
                vector_store = VectorStore()
                results = vector_store.search(job_description, top_k=50) # Get top 50 matches
                return render(request, 'jd_matcher.html', {'results': results, 'job_description': job_description})
            except Exception as e:
                messages.error(request, f"Error during matching: {e}")
                
    return render(request, 'jd_matcher.html')

def homepage(request):
    if request.method == 'POST':
        # Removed Resume.objects.all().delete() to maintain history
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.is_ajax()

        if file_form.is_valid():
            resume_ids = []
            
            # Step 1: Fast Serial Save (Disk I/O)
            for file in files:
                try:
                    resume = Resume(resume=file)
                    resume.tag = request.POST.get('tag')
                    resume.save()
                    resume_ids.append(resume.id)
                except IntegrityError:
                    if is_ajax:
                        return JsonResponse({'status': 'error', 'message': f'Duplicate resume found: {file.name}'}, status=400)
                    messages.warning(request, f'Duplicate resume found: {file.name}')
            
            # Step 2: Parallel Processing (Text Extraction + AI)
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {executor.submit(process_single_resume, r_id, request.POST.get('tag')): r_id for r_id in resume_ids}
                # Wait for completion implemented implicitly by view return? No, we should wait if we want to show updated list.
                # But for UX, we might want to return immediately or wait. 
                # Given user asked for parallel, they usually expect faster turnaround.
                # Let's wait for results to ensure list is updated.
                for future in as_completed(futures):
                    pass
            
            if is_ajax:
                return JsonResponse({'status': 'success', 'message': 'Resumes processed successfully'})

            messages.success(request, 'Resumes processed in background!')

            return redirect('resumes_list')
    else:
        file_form = UploadResumeModelForm()
        
    # Calculate Average Processing Time
    avg_time = Resume.objects.aggregate(Avg('processing_time'))['processing_time__avg']
    avg_time = round(avg_time, 2) if avg_time else 0
    
    return render(request, 'home.html', {'form': file_form, 'avg_processing_time': avg_time})

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
    per_page = request.GET.get('per_page', '10')
    if per_page == 'all':
        paginator = Paginator(resumes, resumes.count())
    else:
        try:
            paginator = Paginator(resumes, int(per_page))
        except ValueError:
            paginator = Paginator(resumes, 10)
            
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

def delete_bulk_resumes(request):
    if request.method == 'POST':
        resume_ids = request.POST.getlist('bulk_delete')
        if resume_ids:
            Resume.objects.filter(id__in=resume_ids).delete()
            messages.success(request, f'{len(resume_ids)} resumes deleted successfully!')
        else:
            messages.warning(request, 'No resumes selected for deletion.')
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

# --- RAG Chat View ---
from .agents.rag_agent import RAGAgent

def chat_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if not query:
            return JsonResponse({'error': 'No query provided'}, status=400)
        
        try:
            agent = RAGAgent()
            answer = agent.chat(query)
            return JsonResponse({'answer': answer})
        except Exception as e:
            print(f"Chat Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'chat.html')