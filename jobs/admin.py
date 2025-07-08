from django.contrib import admin
from .models import JobCategory, Job, JobApplication

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'experience_level', 'location', 'is_active', 'created_at']
    list_filter = ['job_type', 'experience_level', 'is_active', 'created_at', 'category']
    search_fields = ['title', 'company__company_name', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__first_name', 'applicant__last_name']
    readonly_fields = ['applied_at', 'updated_at']
