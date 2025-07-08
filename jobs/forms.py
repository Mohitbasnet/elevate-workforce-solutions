from django import forms
from .models import Job, JobApplication, JobCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'category', 'description', 'requirements', 'responsibilities', 
                 'job_type', 'experience_level', 'salary_min', 'salary_max', 'location', 'application_deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'salary_min': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'salary_max': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
            ),
            'description',
            'requirements',
            'responsibilities',
            Row(
                Column('job_type', css_class='form-group col-md-4 mb-0'),
                Column('experience_level', css_class='form-group col-md-4 mb-0'),
                Column('application_deadline', css_class='form-group col-md-4 mb-0'),
            ),
            Div(
                Row(
                    Column('salary_min', css_class='form-group col-md-6 mb-0'),
                    Column('salary_max', css_class='form-group col-md-6 mb-0'),
                ),
                css_class='salary-section'
            ),
            Submit('submit', 'Post Job', css_class='btn btn-success')
        )

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('cover_letter',)
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your cover letter here...'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'cover_letter',
            Submit('submit', 'Apply for Job', css_class='btn btn-primary')
        )

class JobSearchForm(forms.Form):
    title = forms.CharField(
        max_length=200, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Job title or keywords'})
    )
    location = forms.CharField(
        max_length=200, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    category = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
        required=False
    )
    experience_level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Job.EXPERIENCE_CHOICES,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('location', css_class='form-group col-md-4 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('job_type', css_class='form-group col-md-6 mb-0'),
                Column('experience_level', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Search Jobs', css_class='btn btn-primary')
        ) 