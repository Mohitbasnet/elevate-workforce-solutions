from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, CompanyProfile, JobSeekerProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            'user_type',
            Submit('submit', 'Register', css_class='btn btn-primary')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'phone',
            'address',
            'profile_picture',
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ('company_name', 'company_description', 'website', 'company_size', 'industry', 'established_year')
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
            'established_year': forms.NumberInput(attrs={'min': 1800, 'max': 2024}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'company_name',
            'company_description',
            Row(
                Column('website', css_class='form-group col-md-6 mb-0'),
                Column('industry', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('company_size', css_class='form-group col-md-6 mb-0'),
                Column('established_year', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Update Company Profile', css_class='btn btn-primary')
        )

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('first_name', 'last_name', 'date_of_birth', 'resume', 'skills', 'experience_years', 'education')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter skills separated by commas'}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                Column('experience_years', css_class='form-group col-md-6 mb-0'),
            ),
            'resume',
            'skills',
            'education',
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        ) 