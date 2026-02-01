from django.shortcuts import render, redirect
from .ai_service import get_resume_insights
from .agents.optimization_agent import OptimizationAgent
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

from django.contrib.auth import login
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            
            if user.role == 'CANDIDATE':
                return redirect('candidates:candidate_onboarding')
            
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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
                    'file_url': resume.resume.url if resume.resume else '',
                    'user_id': resume.user.id if resume.user else None
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

@login_required
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
                results = vector_store.search(job_description, top_k=50, user_id=request.user.id) # Get top 50 matches
                return render(request, 'jd_matcher.html', {'results': results, 'job_description': job_description})
            except Exception as e:
                messages.error(request, f"Error during matching: {e}")
                
    return render(request, 'jd_matcher.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def homepage(request):
    """
    Redirects users to their appropriate dashboard based on role.
    """
    user = request.user
    
    if user.role == 'CANDIDATE':
        if hasattr(user, 'candidate_profile'):
            return redirect('candidates:candidate_detail', pk=user.candidate_profile.id)
        return redirect('candidates:candidate_onboarding')
        
    elif user.role in ['ADMIN', 'RECRUITER']:
        return redirect('resumes_list')
        
    elif user.role == 'CLIENT':
        return redirect('job_list')
        
    # Default fallback
    return redirect('resumes_list')

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    # Calculate global average processing time for social proof
    avg_time = Resume.objects.all().aggregate(Avg('processing_time'))['processing_time__avg']
    avg_time = round(avg_time, 2) if avg_time else 0
    
    return render(request, 'landing.html', {'avg_processing_time': avg_time})

def index(request):
    """
    Root view that dispatches to landing page or homepage based on auth.
    """
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        return landing_page(request)

from candidates.models import Candidate

@login_required
def resumes_list(request):
    # 1. Base QuerySet
    if request.user.role in ['ADMIN', 'RECRUITER']:
        candidates = Candidate.objects.all().order_by('-created_at')
    else:
        candidates = Candidate.objects.filter(created_by=request.user).order_by('-created_at')
    
    # 2. Filtering (DB Level)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        candidates = candidates.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(skills__icontains=search_query)
        )

    selected_tag = request.GET.get('tag', '')
    if selected_tag:
        candidates = candidates.filter(status=selected_tag)

    # 3. Pagination
    per_page = request.GET.get('per_page', '10')
    if per_page == 'all':
        paginator = Paginator(candidates, max(len(candidates), 1))
    else:
        try:
            paginator = Paginator(candidates, int(per_page))
        except ValueError:
            paginator = Paginator(candidates, 10)
            
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'resumes': page_obj,
        'tags': ['ACTIVE', 'PAUSED', 'PLACED'], 
        'selected_tag': selected_tag,
        'search_query': search_query,
    }
    return render(request, 'resumes_list.html', context)

@login_required
def delete_resume(request, pk):
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
    except Resume.DoesNotExist:
        messages.warning(request, 'Resume not found or access denied.')
    return redirect('resumes_list')

@login_required
def delete_bulk_resumes(request):
    if request.method == 'POST':
        resume_ids = request.POST.getlist('bulk_delete')
        if resume_ids:
            # Bug fix: Use Candidate model, not Resume
            deleted_count, _ = Candidate.objects.filter(id__in=resume_ids).delete()
            messages.success(request, f'{deleted_count} candidates deleted successfully!')
        else:
            messages.warning(request, 'No resumes selected for deletion.')
    return redirect('resumes_list')

@login_required
def view_resume(request, pk):
    try:
        if request.user.role in ['ADMIN', 'RECRUITER']:
             resume = Candidate.objects.get(pk=pk)
        else:
             resume = Candidate.objects.get(pk=pk, created_by=request.user)
             
        # Adapter for template compatibility (template expects resume.resume.url)
        # Candidate has resume_file
        resume.resume = resume.resume_file
        
    except Candidate.DoesNotExist:
        messages.warning(request, 'Resume not found or access denied.')
        return redirect('resumes_list')
    
    return render(request, 'pdf_viewer.html', {'resume': resume})


@login_required
def update_resume(request, pk):
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
    except Resume.DoesNotExist:
        messages.warning(request, 'Resume not found or access denied.')
        return redirect('resumes_list')
        
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
@login_required
def export_resumes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resumes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Mobile Number', 'Tag', 'Education', 'Skills', 'Company Names', 'Designation', 'Experience', 'Uploaded On'])

    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_on')

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

@login_required
def chat_view(request):
    if request.method == 'POST':
        # Check if it's a reset request
        if request.POST.get('reset') == 'true':
            request.session['chat_history'] = []
            return JsonResponse({'status': 'success', 'message': 'Chat history cleared'})

        query = request.POST.get('query')
        if not query:
            return JsonResponse({'error': 'No query provided'}, status=400)
        
        try:
            # 1. Get History from Session
            history = request.session.get('chat_history', [])
            
            agent = RAGAgent()
            
            # 2. Pass History to Agent & User ID
            answer = agent.chat(query, history=history, user_id=request.user.id)
            
            # 3. Update History
            history.append({'role': 'User', 'content': query})
            history.append({'role': 'AI', 'content': answer})
            
            # 4. Save back to Session
            request.session['chat_history'] = history
            
            return JsonResponse({'answer': answer})
        except Exception as e:
            print(f"Chat Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'chat.html')

@login_required
def resume_optimizer(request):
    """
    View to optimize a selected resume against a Job Description.
    """
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_on')
    results = None
    selected_resume_id = None
    job_description = ""

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        job_description = request.POST.get('job_description')
        selected_resume_id = int(resume_id) if resume_id else None

        if resume_id and job_description:
            try:
                resume = Resume.objects.get(id=resume_id, user=request.user)
                file_path = os.path.join(settings.MEDIA_ROOT, resume.resume.name)
                ext = os.path.splitext(file_path)[1]
                
                # Extract text from the resume file
                resume_text = extract_text(file_path, ext)
                
                # Use OptimizationAgent to get suggestions
                agent = OptimizationAgent()
                results = agent.optimize_resume(resume_text, job_description)
                
            except Resume.DoesNotExist:
                messages.error(request, "Selected resume not found.")
            except Exception as e:
                messages.error(request, f"Error during optimization: {e}")
        else:
            messages.warning(request, "Please select a resume and provide a job description.")

    return render(request, 'optimizer.html', {
        'resumes': resumes,
        'results': results,
        'selected_resume_id': selected_resume_id,
        'job_description': job_description
    })

from .agents.comparison_agent import ComparisonAgent

@login_required
def compare_candidates(request):
    """
    View to compare selected candidates using AI.
    """
    # 1. Permission Check
    if request.user.role not in ['ADMIN', 'RECRUITER']:
         messages.error(request, "Access Denied: Only Recruiters can compare candidates.")
         return redirect('resumes_list')

    if request.method == 'POST':
        # 2. Get Selected IDs
        candidate_ids = request.POST.getlist('bulk_delete') # Reusing the checkbox name from the list view
        
        if not candidate_ids or len(candidate_ids) < 2:
            messages.warning(request, "Please select at least 2 candidates to compare.")
            return redirect('resumes_list')
            
        # Limit to reasonable number to avoid token limits
        if len(candidate_ids) > 5:
             messages.warning(request, "You can compare a maximum of 2 candidates at a time.")
             return redirect('resumes_list')

        # 3. Fetch Data
        candidates = Candidate.objects.filter(id__in=candidate_ids)
        
        # Prepare data for agent
        candidates_data = []
        for cand in candidates:
            candidates_data.append({
                'name': cand.name,
                'skills': cand.skills,
                'experience': f"{cand.experience_years} Years", # Formatted as string
                'education': cand.education,
                'ai_summary': cand.ai_summary
            })
            
        # 4. Call Agent
        try:
            agent = ComparisonAgent()
            comparison_result = agent.compare_candidates(candidates_data)
            
            if 'error' in comparison_result:
                 messages.error(request, f"AI Error: {comparison_result['error']}")
                 return redirect('resumes_list')
                 
            return render(request, 'comparison_report.html', {
                'comparison': comparison_result,
                'candidates': candidates
            })
            
        except Exception as e:
            messages.error(request, f"System Error: {e}")
            return redirect('resumes_list')
            
    return redirect('resumes_list')