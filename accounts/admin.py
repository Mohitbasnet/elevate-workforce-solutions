from django.contrib import admin
from .models import UserProfile, CompanyProfile, JobSeekerProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'company_size', 'established_year']
    list_filter = ['industry', 'company_size']
    search_fields = ['company_name', 'industry']

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'experience_years']
    list_filter = ['experience_years']
    search_fields = ['first_name', 'last_name', 'skills']
