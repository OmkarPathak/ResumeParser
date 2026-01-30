from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate, Application, Interview
from jobs.models import Job
from .forms import CandidateUploadForm, InterviewForm
from django.conf import settings
import os
from parser_app.utils import extract_text
from parser_app.ai_service import get_resume_insights
from parser_app.ai_service import get_resume_insights

@login_required
def candidate_list(request):
    # Candidates should not see the list of other candidates
    if request.user.role == 'CANDIDATE':
        if hasattr(request.user, 'candidate_profile'):
            return redirect('candidates:candidate_detail', pk=request.user.candidate_profile.id)
        return redirect('candidates:candidate_onboarding')

    # Recruiters and Admins see all candidates.
    if request.user.role in ['ADMIN', 'RECRUITER']:
        candidates = Candidate.objects.all().order_by('-created_at')
    else:
        candidates = Candidate.objects.filter(created_by=request.user).order_by('-created_at')
        
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

@login_required
def upload_candidate(request):
    if request.method == 'POST':
        form = CandidateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.created_by = request.user
            candidate.name = candidate.resume_file.name # Temporary name
            candidate.save()
            
            # --- Trigger Parsing Logic (Synchronous for now) ---
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, candidate.resume_file.name)
                ext = os.path.splitext(file_path)[1]
                
                # 1. Extract Text
                text = extract_text(file_path, ext)
                
                # 2. Extract Info via AI
                data = get_resume_insights(text)
                
                if data:
                    candidate.name = data.get('name') or candidate.name
                    candidate.email = data.get('email')
                    
                    # --- DUPLICATE CHECK ---
                    if candidate.email:
                        candidate.email = candidate.email.strip().lower()
                        existing_candidate = Candidate.objects.filter(email__iexact=candidate.email).exclude(id=candidate.id).first()
                        if existing_candidate:
                            messages.warning(request, f"Candidate with email {candidate.email} already exists. Redirected to existing profile.")
                            # Delete the temporary record we just created
                            candidate.delete()
                            return redirect('candidates:candidate_detail', pk=existing_candidate.id)
                    # -----------------------

                    candidate.phone = data.get('mobile_number')
                    candidate.skills = ', '.join(data.get('skills')) if isinstance(data.get('skills'), list) else data.get('skills')
                    candidate.education = ', '.join(data.get('education')) if isinstance(data.get('education'), list) else data.get('education')
                    candidate.ai_summary = data.get('ai_summary')
                    candidate.ai_strengths = data.get('ai_strengths')
                    
                    # Clean experience string to int
                    exp_raw = data.get('total_experience')
                    exp_years = 0
                    if isinstance(exp_raw, (int, float)):
                        exp_years = int(exp_raw)
                    elif isinstance(exp_raw, str):
                        # Extract first number found
                        import re
                        match = re.search(r'\d+', exp_raw)
                        if match:
                            exp_years = int(match.group())
                    
                    candidate.experience_years = exp_years
                    candidate.save()
                    messages.success(request, f"Candidate {candidate.name} uploaded and parsed successfully!")
                else:
                    messages.warning(request, "Resume uploaded but AI parsing failed to return data.")
            except Exception as e:
                print(f"Parsing Error: {e}")
                messages.error(request, f"Error during parsing: {e}")
            
            return redirect('resumes_list')
    else:
        form = CandidateUploadForm()
    return render(request, 'candidates/candidate_form.html', {'form': form, 'title': 'Upload Candidate'})

@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    # Access control
    if request.user.role != 'ADMIN' and candidate.created_by != request.user:
        # Check if linked to a job user owns (Activity log logic usually)
        pass
        
    # Get available jobs for submission
    available_jobs = Job.objects.filter(status=Job.ACTIVE)
    if request.user.role == 'RECRUITER':
        # Recruiters can submit to any active job they have access to? Or only their clients?
        # SOW says: "Recruiters can submit a candidate to multiple clients."
        pass
    
    # Get existing applications
    applications = candidate.applications.all()
        
    return render(request, 'candidates/candidate_detail.html', {
        'candidate': candidate, 
        'available_jobs': available_jobs,
        'applications': applications
    })

@login_required
def submit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if request.method == 'POST':
        job_id = request.POST.get('job')
        job = get_object_or_404(Job, pk=job_id)
        
        # Check if already applied
        if Application.objects.filter(candidate=candidate, job=job).exists():
            messages.warning(request, f"{candidate.name} has already applied for this job.")
        else:
            Application.objects.create(candidate=candidate, job=job, status='APPLIED')
            messages.success(request, f"{candidate.name} submitted to {job.title} successfully.")
            
        return redirect('candidates:candidate_detail', pk=candidate.id)
    return redirect('candidates:candidate_detail', pk=candidate.id)

@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.interviewer = request.user # Default to current user, or select from form
            interview.save()
            
            # Update Application Status
            application.status = 'INTERVIEW'
            application.save()
            
            messages.success(request, 'Interview scheduled successfully!')
            return redirect('candidates:candidate_detail', pk=application.candidate.id)
    else:
        form = InterviewForm()
    
    return render(request, 'candidates/interview_form.html', {'form': form, 'application': application, 'title': 'Schedule Interview'})

@login_required
def update_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview updated successfully!')
            return redirect('candidates:candidate_detail', pk=interview.application.candidate.id)
    else:
        form = InterviewForm(instance=interview)
    
    return render(request, 'candidates/interview_form.html', {'form': form, 'application': interview.application, 'title': 'Update Interview'})

@login_required
def apply_to_job(request, job_id):
    if request.user.role != 'CANDIDATE':
        messages.error(request, "Only candidates can apply to jobs.")
        return redirect('job_list')
        
    job = get_object_or_404(Job, pk=job_id)
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        messages.error(request, "Please create a candidate profile first.")
        # Redirect to create profile or home
        return redirect('homepage') 

    # Check if already applied
    if Application.objects.filter(candidate=candidate, job=job).exists():
        messages.warning(request, f"You have already applied for {job.title}.")
    else:
        Application.objects.create(candidate=candidate, job=job, status='APPLIED')
        messages.success(request, f"Successfully applied to {job.title}!")
        
    return redirect('job_list')

@login_required
def candidate_onboarding(request):
    # If already has profile, redirect to detail
    if hasattr(request.user, 'candidate_profile'):
        messages.info(request, "You already have a profile.")
        return redirect('candidates:candidate_detail', pk=request.user.candidate_profile.id)

    if request.method == 'POST':
        form = CandidateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user  # Link the specific user account
            candidate.created_by = request.user
            candidate.save()
            
            # --- Trigger Parsing Logic ---
            try:
                # Assuming simple sync parsing for onboarding to give immediate feedback
                file_path = os.path.join(settings.MEDIA_ROOT, candidate.resume_file.name)
                ext = os.path.splitext(file_path)[1]
                resume_text = extract_text(file_path, ext)
                data = get_resume_insights(resume_text)
                
                if data:
                    candidate.name = data.get('name') or request.user.first_name or request.user.username
                    candidate.email = data.get('email') or request.user.email
                    
                    # --- DUPLICATE / CLAIM CHECK ---
                    if candidate.email:
                        candidate.email = candidate.email.strip().lower()
                        existing_candidate = Candidate.objects.filter(email__iexact=candidate.email).exclude(id=candidate.id).first()
                        
                        if existing_candidate:
                            # Case 1: Existing profile has no user (uploaded by recruiter) -> CLAIM IT
                            if existing_candidate.user is None:
                                existing_candidate.user = request.user
                                # Optional: Update other fields if empty? For now, trust existing data or overwrite?
                                # Let's assume existing data is good, but we link the user.
                                existing_candidate.save()
                                
                                messages.info(request, f"We found an existing profile for {candidate.email} and linked it to your account!")
                                candidate.delete() # Delete the temp one
                                return redirect('candidates:candidate_detail', pk=existing_candidate.id)
                            
                            # Case 2: Existing profile ALREADY has a user -> CONFLICT
                            elif existing_candidate.user != request.user:
                                messages.error(request, f"A profile with email {candidate.email} already exists and is owned by another user.")
                                candidate.delete() 
                                return redirect('candidates:candidate_onboarding')
                            
                            # Case 3: existing_candidate.user == request.user (Shouldn't happen if check at top works, but safe to handle)
                            else:
                                candidate.delete()
                                return redirect('candidates:candidate_detail', pk=existing_candidate.id)
                    # --------------------------------

                    candidate.phone = data.get('mobile_number')
                    candidate.skills = ', '.join(data.get('skills')) if isinstance(data.get('skills'), list) else data.get('skills')
                    
                    # Clean experience string to int
                    exp_raw = data.get('total_experience')
                    exp_years = 0
                    if isinstance(exp_raw, (int, float)):
                        exp_years = int(exp_raw)
                    elif isinstance(exp_raw, str):
                        # Extract first number found
                        import re
                        match = re.search(r'\d+', exp_raw)
                        if match:
                            exp_years = int(match.group())
                    
                    candidate.experience_years = exp_years
                    candidate.education = ', '.join(data.get('education')) if isinstance(data.get('education'), list) else data.get('education')
                    candidate.ai_summary = data.get('ai_summary')
                    candidate.ai_strengths = data.get('ai_strengths')
                    candidate.save()
                    
                    messages.success(request, "Profile created and resume parsed successfully!")
            except Exception as e:
                print(f"Error parsing resume during onboarding: {e}")
                messages.warning(request, "Profile created, but resume parsing failed. Please update details manually.")
            
            return redirect('candidates:candidate_detail', pk=candidate.id)
    else:
        form = CandidateUploadForm()
    
    return render(request, 'candidates/onboarding.html', {'form': form})

@login_required
def candidate_update(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    
    # Check permissions (only owner or admin can edit)
    if request.user != candidate.created_by and request.user.role != 'ADMIN':
        messages.error(request, "You do not have permission to edit this profile.")
        return redirect('candidates:candidate_detail', pk=candidate.id)

    if request.method == 'POST':
        from .forms import CandidateUpdateForm
        form = CandidateUpdateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('candidates:candidate_detail', pk=candidate.id)
    else:
        from .forms import CandidateUpdateForm
        form = CandidateUpdateForm(instance=candidate)
    
    return render(request, 'candidates/candidate_form.html', {'form': form, 'title': 'Edit Profile'})

@login_required
def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    
    # Permission check: Admins and Recruiters can delete any; Owners can delete their own
    if request.user.role not in ['ADMIN', 'RECRUITER'] and request.user != candidate.created_by:
        messages.error(request, "Permission denied.")
        return redirect('resumes_list')
        
    candidate.delete()
    messages.success(request, "Candidate deleted successfully.")
    return redirect('resumes_list')

@login_required
def candidate_settings(request):
    """
    Redirects candidates to their profile edit page if it exists,
    otherwise to completion/onboarding.
    """
    if request.user.role == 'CANDIDATE':
        if hasattr(request.user, 'candidate_profile'):
            return redirect('candidates:candidate_update', pk=request.user.candidate_profile.id)
        else:
            return redirect('candidates:candidate_onboarding')
            
    # Fallback for other roles (functionality not defined yet)
    messages.info(request, "Settings not available for this role yet.")
    return redirect('homepage')
