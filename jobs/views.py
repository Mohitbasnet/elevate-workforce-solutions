from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db import models
from django.http import HttpResponseForbidden, Http404
from .models import Job, JobApplication, JobCategory
from .forms import JobForm, JobApplicationForm, JobSearchForm
from accounts.models import UserProfile, CompanyProfile, JobSeekerProfile

def job_list(request):
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    jobs = Job.objects.filter(is_active=True).select_related('company', 'category')
    form = JobSearchForm(request.GET)
    
    # Enhanced filtering
    if form.is_valid():
        title = form.cleaned_data.get('title')
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')
        experience_level = form.cleaned_data.get('experience_level')
        
        if title:
            jobs = jobs.filter(Q(title__icontains=title) | Q(description__icontains=title) | Q(requirements__icontains=title))
        if location:
            jobs = jobs.filter(location__icontains=location)
        if category:
            jobs = jobs.filter(category=category)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
    
    # Additional filters from GET parameters
    salary_range = request.GET.get('salary_range')
    if salary_range:
        if salary_range == '0-50000':
            jobs = jobs.filter(salary_max__lte=50000)
        elif salary_range == '50000-100000':
            jobs = jobs.filter(salary_min__gte=50000, salary_max__lte=100000)
        elif salary_range == '100000-200000':
            jobs = jobs.filter(salary_min__gte=100000, salary_max__lte=200000)
        elif salary_range == '200000+':
            jobs = jobs.filter(salary_min__gte=200000)
    
    # Date posted filter
    date_posted = request.GET.get('date_posted')
    if date_posted:
        days = int(date_posted)
        cutoff_date = timezone.now() - timedelta(days=days)
        jobs = jobs.filter(created_at__gte=cutoff_date)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        jobs = jobs.order_by('-created_at')
    elif sort_by == 'oldest':
        jobs = jobs.order_by('created_at')
    elif sort_by == 'salary_high':
        jobs = jobs.order_by('-salary_max', '-salary_min')
    elif sort_by == 'salary_low':
        jobs = jobs.order_by('salary_min', 'salary_max')
    elif sort_by == 'alphabetical':
        jobs = jobs.order_by('title')
    else:
        jobs = jobs.order_by('-created_at')
    
    # Note: total_applications is already available as a property method in the Job model
    
    # Pagination with dynamic per_page
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in [10, 20, 50]:
        per_page = 10
        
    paginator = Paginator(jobs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = JobCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'categories': categories,
        'total_jobs': jobs.count(),
        'current_filters': {
            'title': request.GET.get('title', ''),
            'location': request.GET.get('location', ''),
            'category': request.GET.get('category', ''),
            'job_type': request.GET.get('job_type', ''),
            'experience_level': request.GET.get('experience_level', ''),
            'salary_range': request.GET.get('salary_range', ''),
            'date_posted': request.GET.get('date_posted', ''),
            'sort': sort_by,
            'per_page': per_page,
        }
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, pk):
    # Allow job owners to view inactive jobs, but require active jobs for others
    if request.user.is_authenticated:
        # Use select_related to optimize the query
        job = get_object_or_404(Job.objects.select_related('company__user_profile', 'category', 'posted_by'), pk=pk)
        # If the user doesn't own the job and it's inactive, return 404
        if job.posted_by != request.user and not job.is_active:
            raise Http404("Job not found")
    else:
        job = get_object_or_404(Job.objects.select_related('company__user_profile', 'category', 'posted_by'), pk=pk, is_active=True)
    
    user_has_applied = False
    can_apply = False
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type == 'job_seeker':
                job_seeker_profile = JobSeekerProfile.objects.get(user_profile=user_profile)
                # Optimize the application check
                user_has_applied = JobApplication.objects.filter(
                    job=job, applicant=job_seeker_profile
                ).exists()
                can_apply = not user_has_applied and job.is_active
        except (UserProfile.DoesNotExist, JobSeekerProfile.DoesNotExist):
            pass
    
    context = {
        'job': job,
        'user_has_applied': user_has_applied,
        'can_apply': can_apply,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    try:
        # Use select_related to reduce database queries
        user_profile = UserProfile.objects.select_related('user').get(user=request.user)
        if user_profile.user_type != 'job_seeker':
            messages.error(request, 'Only job seekers can apply for jobs.')
            return redirect('jobs:job_detail', pk=pk)
        
        job_seeker_profile = JobSeekerProfile.objects.get(user_profile=user_profile)
        
        # Check if already applied (optimized query)
        existing_application = JobApplication.objects.filter(job=job, applicant=job_seeker_profile).first()
        if existing_application:
            messages.warning(request, 'You have already applied for this job.')
            return redirect('jobs:job_detail', pk=pk)
        
        if request.method == 'POST':
            form = JobApplicationForm(request.POST)
            if form.is_valid():
                try:
                    print(f"DEBUG: Starting job application for job {job.id}")
                    application = form.save(commit=False)
                    application.job = job
                    application.applicant = job_seeker_profile
                    application.save()
                    print(f"DEBUG: Application saved successfully")
                    
                    # Send notification to company
                    try:
                        from user_notifications.utils import notify_job_application_received
                        notify_job_application_received(job, job_seeker_profile, job.posted_by)
                        print(f"DEBUG: Notification sent successfully")
                    except Exception as e:
                        # Don't let notification errors stop application submission
                        print(f"Notification error: {e}")
                    
                    print(f"DEBUG: About to show success message and redirect")
                    messages.success(request, 'Your application has been submitted successfully!')
                    return redirect('jobs:job_detail', pk=pk)
                except Exception as e:
                    messages.error(request, 'There was an error submitting your application. Please try again.')
                    # Log the error for debugging
                    print(f"Job application error: {e}")
        else:
            form = JobApplicationForm()
        
        context = {
            'job': job,
            'form': form,
        }
        return render(request, 'jobs/job_apply.html', context)
        
    except (UserProfile.DoesNotExist, JobSeekerProfile.DoesNotExist):
        messages.error(request, 'Please complete your profile first.')
        return redirect('accounts:profile_setup')

@login_required
def job_create(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'company':
            messages.error(request, 'Only companies can post jobs.')
            return redirect('jobs:job_list')
        
        company_profile = CompanyProfile.objects.get(user_profile=user_profile)
        
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.company = company_profile
                job.posted_by = request.user
                job.save()
                
                # Send notification to relevant job seekers (async to prevent delays)
                try:
                    from user_notifications.utils import notify_new_job_posted
                    notify_new_job_posted(job)
                except Exception as e:
                    # Don't let notification errors stop job creation
                    print(f"Notification error: {e}")
                
                messages.success(request, 'Job posted successfully!')
                return redirect('jobs:job_detail', pk=job.pk)
        else:
            form = JobForm()
        
        return render(request, 'jobs/job_create.html', {'form': form})
        
    except (UserProfile.DoesNotExist, CompanyProfile.DoesNotExist):
        messages.error(request, 'Please complete your company profile first.')
        return redirect('accounts:profile_setup')

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user owns this job
    if job.posted_by != request.user:
        return HttpResponseForbidden("You don't have permission to edit this job.")
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            # Handle is_active checkbox
            job.is_active = 'is_active' in request.POST
            job.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/job_edit.html', {'form': form, 'job': job})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user owns this job
    if job.posted_by != request.user:
        return HttpResponseForbidden("You don't have permission to delete this job.")
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('accounts:dashboard')
    
    return render(request, 'jobs/job_delete.html', {'job': job})

@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user owns this job
    if job.posted_by != request.user:
        return HttpResponseForbidden("You don't have permission to view these applications.")
    
    applications = JobApplication.objects.filter(job=job).select_related('applicant__user_profile__user')
    
    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'jobs/job_applications.html', context)

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Check if user owns the job
    if application.job.posted_by != request.user:
        return HttpResponseForbidden("You don't have permission to update this application.")
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(JobApplication.STATUS_CHOICES):
            old_status = application.status
            application.status = status
            application.save()
            
            # Send notification to job seeker about status change
            from user_notifications.utils import notify_application_status_change
            notify_application_status_change(application, status)
            
            messages.success(request, f'Application status updated to {application.get_status_display()}.')
    
    return redirect('jobs:job_applications', pk=application.job.pk)

def home(request):
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    total_jobs = Job.objects.filter(is_active=True).count()
    total_companies = CompanyProfile.objects.count()
    total_applications = JobApplication.objects.count()
    
    context = {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_applications': total_applications,
    }
    return render(request, 'jobs/home.html', context)
