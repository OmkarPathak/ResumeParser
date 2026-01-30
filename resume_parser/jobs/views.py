from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Client
from .forms import JobForm, JobSearchForm, ClientForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def client_create_ajax(request):
    form = ClientForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        # Check for duplicate
        if Client.objects.filter(name__iexact=name, owner=request.user).exists():
             return JsonResponse({'success': False, 'error': 'Client with this name already exists.'})
        
        client = form.save(commit=False)
        client.owner = request.user
        client.save()
        return JsonResponse({'success': True, 'id': client.id, 'name': client.name})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data.'})

@login_required
def job_list(request):
    jobs = Job.objects.all()
    
    # RBAC: Clients only see their jobs
    # RBAC: Clients only see their jobs
    if request.user.role == 'CLIENT':
        # jobs = jobs.filter(client__owner=request.user) 
        # TODO: Link Client User to Client Model properly. For now, showing all for demo transparency or empty.
        # Assuming we fixed Client-User link, we'd use it here.
        pass
    elif request.user.role == 'CANDIDATE':
        jobs = jobs.filter(status='ACTIVE')

    # Search
    form = JobSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        status = form.cleaned_data.get('status')
        
        if q:
            jobs = jobs.filter(Q(title__icontains=q) | Q(skills_required__icontains=q) | Q(location__icontains=q))
        if status:
            jobs = jobs.filter(status=status)

    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'form': form})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            
            # If user is Client, assign their Client object automatically
            if request.user.role == 'CLIENT':
                # Assuming 1:1 mapping or taking first. 
                # In real app, might need a way to select if they own multiple.
                client = Client.objects.filter(owner=request.user).first()
                if client:
                    job.client = client
                else:
                    messages.error(request, "No Client profile found for your account.")
                    return redirect('job_list')

            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
    else:
        form = JobForm(user=request.user)
    
    # Pass ClientForm for the modal
    client_form = ClientForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'client_form': client_form, 'title': 'Create Job'})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_list')
    else:
        form = JobForm(instance=job, user=request.user)
        
    client_form = ClientForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'client_form': client_form, 'title': 'Update Job'})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
