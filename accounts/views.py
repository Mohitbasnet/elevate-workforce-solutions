from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm, UserProfileForm, CompanyProfileForm, JobSeekerProfileForm
from .models import UserProfile, CompanyProfile, JobSeekerProfile
from jobs.models import Job, JobApplication

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('accounts:profile_setup')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_setup(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # If user_type is not set, we need to show a selection form
    if not user_profile.user_type:
        if request.method == 'POST' and 'user_type' in request.POST:
            user_profile.user_type = request.POST['user_type']
            user_profile.save()
            # Continue with the rest of the setup process
        else:
            return render(request, 'accounts/profile_setup.html', {
                'show_user_type_selection': True,
                'user_profile': user_profile
            })
    
    if user_profile.user_type == 'company':
        company_profile, created = CompanyProfile.objects.get_or_create(user_profile=user_profile)
        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            company_form = CompanyProfileForm(request.POST, instance=company_profile)
            if user_form.is_valid() and company_form.is_valid():
                user_form.save()
                company_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:dashboard')
        else:
            user_form = UserProfileForm(instance=user_profile)
            company_form = CompanyProfileForm(instance=company_profile)
        return render(request, 'accounts/profile_setup.html', {
            'user_form': user_form,
            'company_form': company_form,
            'user_type': 'company'
        })
    
    else:  # job_seeker
        job_seeker_profile, created = JobSeekerProfile.objects.get_or_create(user_profile=user_profile)
        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            job_seeker_form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile)
            if user_form.is_valid() and job_seeker_form.is_valid():
                user_form.save()
                job_seeker_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:dashboard')
        else:
            user_form = UserProfileForm(instance=user_profile)
            job_seeker_form = JobSeekerProfileForm(instance=job_seeker_profile)
        return render(request, 'accounts/profile_setup.html', {
            'user_form': user_form,
            'job_seeker_form': job_seeker_form,
            'user_type': 'job_seeker'
        })

@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.warning(request, 'Please set up your profile first.')
        return redirect('accounts:profile_setup')
    
    if user_profile.user_type == 'company':
        try:
            company_profile = CompanyProfile.objects.get(user_profile=user_profile)
            posted_jobs = Job.objects.filter(company=company_profile).order_by('-created_at')
            total_applications = JobApplication.objects.filter(job__company=company_profile).count()
            context = {
                'user_profile': user_profile,
                'company_profile': company_profile,
                'posted_jobs': posted_jobs,
                'total_applications': total_applications,
            }
            return render(request, 'accounts/company_dashboard.html', context)
        except CompanyProfile.DoesNotExist:
            messages.warning(request, 'Please complete your company profile first.')
            return redirect('accounts:profile_setup')
    
    else:  # job_seeker
        try:
            job_seeker_profile = JobSeekerProfile.objects.get(user_profile=user_profile)
            applications = JobApplication.objects.filter(applicant=job_seeker_profile).order_by('-applied_at')
            
            # Calculate statistics
            pending_applications = applications.filter(status='pending').count()
            interview_applications = applications.filter(status='interview').count()
            hired_applications = applications.filter(status='hired').count()
            
            context = {
                'user_profile': user_profile,
                'job_seeker_profile': job_seeker_profile,
                'applications': applications,
                'pending_applications': pending_applications,
                'interview_applications': interview_applications,
                'hired_applications': hired_applications,
            }
            return render(request, 'accounts/job_seeker_dashboard.html', context)
        except JobSeekerProfile.DoesNotExist:
            messages.warning(request, 'Please complete your profile first.')
            return redirect('accounts:profile_setup')

@login_required
def profile_edit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.warning(request, 'Please set up your profile first.')
        return redirect('accounts:profile_setup')
    
    if user_profile.user_type == 'company':
        company_profile = get_object_or_404(CompanyProfile, user_profile=user_profile)
        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            company_form = CompanyProfileForm(request.POST, instance=company_profile)
            if user_form.is_valid() and company_form.is_valid():
                user_form.save()
                company_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:dashboard')
        else:
            user_form = UserProfileForm(instance=user_profile)
            company_form = CompanyProfileForm(instance=company_profile)
        return render(request, 'accounts/profile_edit.html', {
            'user_form': user_form,
            'company_form': company_form,
            'user_type': 'company'
        })
    
    else:  # job_seeker
        job_seeker_profile = get_object_or_404(JobSeekerProfile, user_profile=user_profile)
        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            job_seeker_form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile)
            if user_form.is_valid() and job_seeker_form.is_valid():
                user_form.save()
                job_seeker_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:dashboard')
        else:
            user_form = UserProfileForm(instance=user_profile)
            job_seeker_form = JobSeekerProfileForm(instance=job_seeker_profile)
        return render(request, 'accounts/profile_edit.html', {
            'user_form': user_form,
            'job_seeker_form': job_seeker_form,
            'user_type': 'job_seeker'
        })
