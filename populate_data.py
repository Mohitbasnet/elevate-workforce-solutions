#!/usr/bin/env python
"""
Script to populate the Elevate Workforce Solutions database with sample data.
This will create realistic companies, job seekers, jobs, and applications.
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevate_workforce.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, CompanyProfile, JobSeekerProfile
from jobs.models import JobCategory, Job, JobApplication
from django.utils import timezone
from datetime import datetime, timedelta
import random

def create_job_categories():
    """Create job categories"""
    categories = [
        'Information Technology',
        'Finance & Banking',
        'Healthcare & Medical',
        'Marketing & Sales',
        'Engineering',
        'Education & Training',
        'Human Resources',
        'Customer Service',
        'Operations & Management',
        'Design & Creative',
        'Legal & Compliance',
        'Manufacturing',
        'Hospitality & Tourism',
        'Real Estate',
        'Telecommunications'
    ]
    
    print("Creating job categories...")
    for category_name in categories:
        category, created = JobCategory.objects.get_or_create(
            name=category_name,
            defaults={'description': f'Jobs related to {category_name}'}
        )
        if created:
            print(f"  ✓ Created category: {category_name}")

def create_companies():
    """Create sample companies with profiles"""
    companies_data = [
        {
            'username': 'technovation_np',
            'email': 'hr@technovation.com.np',
            'company_name': 'Technovation Nepal',
            'industry': 'Information Technology',
            'company_size': 'medium',
            'description': 'Leading software development company in Nepal specializing in web and mobile applications.',
            'website': 'https://technovation.com.np',
            'established_year': 2015
        },
        {
            'username': 'himalayan_bank',
            'email': 'careers@himalayanbank.com',
            'company_name': 'Himalayan Bank Limited',
            'industry': 'Banking & Finance',
            'company_size': 'large',
            'description': 'One of Nepal\'s premier financial institutions providing comprehensive banking solutions.',
            'website': 'https://himalayanbank.com',
            'established_year': 1993
        },
        {
            'username': 'mercy_hospital',
            'email': 'hr@mercyhospital.org.np',
            'company_name': 'Mercy Hospital',
            'industry': 'Healthcare',
            'company_size': 'medium',
            'description': 'Modern healthcare facility providing quality medical services across Nepal.',
            'website': 'https://mercyhospital.org.np',
            'established_year': 2008
        },
        {
            'username': 'digital_hub_nepal',
            'email': 'jobs@digitalhub.com.np',
            'company_name': 'Digital Hub Nepal',
            'industry': 'Digital Marketing',
            'company_size': 'small',
            'description': 'Creative digital agency helping businesses grow through innovative marketing strategies.',
            'website': 'https://digitalhub.com.np',
            'established_year': 2018
        },
        {
            'username': 'everest_construction',
            'email': 'hr@everestconstruction.com.np',
            'company_name': 'Everest Construction Ltd',
            'industry': 'Construction & Engineering',
            'company_size': 'large',
            'description': 'Leading construction company with expertise in residential and commercial projects.',
            'website': 'https://everestconstruction.com.np',
            'established_year': 2005
        },
        {
            'username': 'smart_education',
            'email': 'careers@smartedu.edu.np',
            'company_name': 'Smart Education Institute',
            'industry': 'Education',
            'company_size': 'medium',
            'description': 'Progressive educational institution focused on modern learning methodologies.',
            'website': 'https://smartedu.edu.np',
            'established_year': 2012
        },
        {
            'username': 'nepal_airlines',
            'email': 'hr@nepalairlines.com.np',
            'company_name': 'Nepal Airlines Corporation',
            'industry': 'Aviation',
            'company_size': 'large',
            'description': 'National flag carrier of Nepal providing domestic and international flights.',
            'website': 'https://nepalairlines.com.np',
            'established_year': 1958
        },
        {
            'username': 'green_energy_nepal',
            'email': 'jobs@greenenergy.com.np',
            'company_name': 'Green Energy Nepal',
            'industry': 'Renewable Energy',
            'company_size': 'medium',
            'description': 'Pioneering renewable energy solutions for sustainable development in Nepal.',
            'website': 'https://greenenergy.com.np',
            'established_year': 2016
        }
    ]
    
    print("Creating companies...")
    created_companies = []
    
    for company_data in companies_data:
        # Create user account
        user, created = User.objects.get_or_create(
            username=company_data['username'],
            defaults={
                'email': company_data['email'],
                'first_name': company_data['company_name'],
                'is_active': True
            }
        )
        
        if created:
            user.set_password('company123')  # Default password
            user.save()
            
            # Create user profile
            user_profile = UserProfile.objects.create(
                user=user,
                user_type='company',
                phone=f"+977-1-{random.randint(4000000, 4999999)}",
                address=f"Kathmandu, Nepal"
            )
            
            # Create company profile
            company_profile = CompanyProfile.objects.create(
                user_profile=user_profile,
                company_name=company_data['company_name'],
                company_description=company_data['description'],
                industry=company_data['industry'],
                company_size=company_data['company_size'],
                website=company_data.get('website'),
                established_year=company_data.get('established_year')
            )
            
            created_companies.append(company_profile)
            print(f"  ✓ Created company: {company_data['company_name']}")
        else:
            print(f"  - Company already exists: {company_data['company_name']}")
    
    return created_companies

def create_job_seekers():
    """Create sample job seekers with profiles"""
    job_seekers_data = [
        {
            'username': 'ramesh_sharma',
            'email': 'ramesh.sharma@email.com',
            'first_name': 'Ramesh',
            'last_name': 'Sharma',
            'skills': 'Python, Django, JavaScript, React, MySQL, Git',
            'experience_years': 3,
            'education': 'Bachelor of Computer Engineering from Tribhuvan University'
        },
        {
            'username': 'priya_thapa',
            'email': 'priya.thapa@email.com',
            'first_name': 'Priya',
            'last_name': 'Thapa',
            'skills': 'Digital Marketing, SEO, Google Analytics, Content Writing, Social Media',
            'experience_years': 2,
            'education': 'Master of Business Administration (MBA) from Kathmandu University'
        },
        {
            'username': 'sujan_karki',
            'email': 'sujan.karki@email.com',
            'first_name': 'Sujan',
            'last_name': 'Karki',
            'skills': 'Java, Spring Boot, Microservices, Docker, Kubernetes, AWS',
            'experience_years': 5,
            'education': 'Master of Computer Applications (MCA) from Pokhara University'
        },
        {
            'username': 'anita_gurung',
            'email': 'anita.gurung@email.com',
            'first_name': 'Anita',
            'last_name': 'Gurung',
            'skills': 'Nursing, Patient Care, Medical Administration, Emergency Response',
            'experience_years': 4,
            'education': 'Bachelor of Nursing from Institute of Medicine, Tribhuvan University'
        },
        {
            'username': 'bikash_shrestha',
            'email': 'bikash.shrestha@email.com',
            'first_name': 'Bikash',
            'last_name': 'Shrestha',
            'skills': 'AutoCAD, Civil Engineering, Project Management, Structural Analysis',
            'experience_years': 6,
            'education': 'Bachelor of Civil Engineering from Nepal Engineering College'
        },
        {
            'username': 'maya_tamang',
            'email': 'maya.tamang@email.com',
            'first_name': 'Maya',
            'last_name': 'Tamang',
            'skills': 'Teaching, Curriculum Development, Student Assessment, Educational Technology',
            'experience_years': 8,
            'education': 'Master of Education from Tribhuvan University'
        },
        {
            'username': 'rohan_poudel',
            'email': 'rohan.poudel@email.com',
            'first_name': 'Rohan',
            'last_name': 'Poudel',
            'skills': 'Financial Analysis, Accounting, Excel, SAP, Risk Management',
            'experience_years': 4,
            'education': 'Bachelor of Business Studies (BBS) from Tribhuvan University'
        },
        {
            'username': 'sunita_rai',
            'email': 'sunita.rai@email.com',
            'first_name': 'Sunita',
            'last_name': 'Rai',
            'skills': 'Graphic Design, Adobe Creative Suite, UI/UX Design, Branding',
            'experience_years': 3,
            'education': 'Bachelor of Fine Arts from Kathmandu University'
        },
        {
            'username': 'kiran_magar',
            'email': 'kiran.magar@email.com',
            'first_name': 'Kiran',
            'last_name': 'Magar',
            'skills': 'HR Management, Recruitment, Training, Employee Relations, Payroll',
            'experience_years': 5,
            'education': 'Master of Business Administration in HR from Ace Institute of Management'
        },
        {
            'username': 'sita_bhandari',
            'email': 'sita.bhandari@email.com',
            'first_name': 'Sita',
            'last_name': 'Bhandari',
            'skills': 'Customer Service, Communication, Problem Solving, CRM Systems',
            'experience_years': 2,
            'education': 'Bachelor of Business Administration from Pokhara University'
        }
    ]
    
    print("Creating job seekers...")
    created_job_seekers = []
    
    for seeker_data in job_seekers_data:
        # Create user account
        user, created = User.objects.get_or_create(
            username=seeker_data['username'],
            defaults={
                'email': seeker_data['email'],
                'first_name': seeker_data['first_name'],
                'last_name': seeker_data['last_name'],
                'is_active': True
            }
        )
        
        if created:
            user.set_password('jobseeker123')  # Default password
            user.save()
            
            # Create user profile
            user_profile = UserProfile.objects.create(
                user=user,
                user_type='job_seeker',
                phone=f"+977-98{random.randint(10000000, 99999999)}",
                address=f"{random.choice(['Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Chitwan'])}, Nepal"
            )
            
            # Create job seeker profile
            job_seeker_profile = JobSeekerProfile.objects.create(
                user_profile=user_profile,
                first_name=seeker_data['first_name'],
                last_name=seeker_data['last_name'],
                skills=seeker_data['skills'],
                experience_years=seeker_data['experience_years'],
                education=seeker_data['education'],
                date_of_birth=datetime(1990 + random.randint(-5, 5), random.randint(1, 12), random.randint(1, 28)).date()
            )
            
            created_job_seekers.append(job_seeker_profile)
            print(f"  ✓ Created job seeker: {seeker_data['first_name']} {seeker_data['last_name']}")
        else:
            print(f"  - Job seeker already exists: {seeker_data['first_name']} {seeker_data['last_name']}")
    
    return created_job_seekers

def create_jobs():
    """Create sample jobs"""
    companies = list(CompanyProfile.objects.all())
    categories = list(JobCategory.objects.all())
    
    if not companies:
        print("No companies found! Please create companies first.")
        return []
    
    jobs_data = [
        {
            'title': 'Senior Full Stack Developer',
            'description': '''We are seeking an experienced Full Stack Developer to join our dynamic team. You will be responsible for developing and maintaining web applications using modern technologies.

Key Responsibilities:
• Develop responsive web applications using React.js and Node.js
• Design and implement RESTful APIs
• Work with databases (MySQL, MongoDB)
• Collaborate with cross-functional teams
• Write clean, maintainable code
• Participate in code reviews and testing''',
            'requirements': '''Required Qualifications:
• Bachelor's degree in Computer Science or related field
• 3+ years of experience in full-stack development
• Proficiency in JavaScript, React, Node.js
• Experience with databases (MySQL, MongoDB)
• Knowledge of Git version control
• Strong problem-solving skills
• Excellent communication skills

Preferred Qualifications:
• Experience with cloud platforms (AWS, Azure)
• Knowledge of Docker and containerization
• Familiarity with Agile methodologies''',
            'responsibilities': '''Daily Responsibilities:
• Develop new features and maintain existing applications
• Collaborate with UI/UX designers for implementation
• Write and maintain technical documentation
• Debug and resolve technical issues
• Optimize application performance
• Mentor junior developers
• Stay updated with latest technologies''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'mid_level',
            'salary_min': 80000,
            'salary_max': 120000,
            'industry_match': 'Information Technology'
        },
        {
            'title': 'Digital Marketing Specialist',
            'description': '''Join our creative team as a Digital Marketing Specialist and help drive our online presence and growth strategies.

We're looking for someone passionate about digital marketing with hands-on experience in SEO, social media, and content marketing.''',
            'requirements': '''• Bachelor's degree in Marketing or related field
• 2+ years of digital marketing experience
• Proficiency in Google Analytics, Google Ads
• Experience with social media marketing
• Strong analytical and communication skills
• Knowledge of SEO best practices''',
            'responsibilities': '''• Develop and execute digital marketing campaigns
• Manage social media accounts and content
• Analyze campaign performance and ROI
• Create engaging content for various platforms
• Collaborate with design team for marketing materials
• Stay updated with digital marketing trends''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'entry_level',
            'salary_min': 40000,
            'salary_max': 60000,
            'industry_match': 'Digital Marketing'
        },
        {
            'title': 'Registered Nurse - ICU',
            'description': '''We are seeking a dedicated Registered Nurse to join our Intensive Care Unit team. The ideal candidate will provide high-quality patient care in a fast-paced environment.''',
            'requirements': '''• Bachelor's degree in Nursing from recognized institution
• Valid nursing license in Nepal
• 2+ years of ICU experience preferred
• BLS and ACLS certification
• Strong clinical skills and attention to detail
• Excellent communication and teamwork abilities''',
            'responsibilities': '''• Provide direct patient care in ICU setting
• Monitor patient vital signs and conditions
• Administer medications as prescribed
• Collaborate with healthcare team
• Maintain accurate patient records
• Educate patients and families
• Follow safety protocols and procedures''',
            'location': 'Lalitpur, Nepal',
            'job_type': 'full_time',
            'experience_level': 'mid_level',
            'salary_min': 60000,
            'salary_max': 85000,
            'industry_match': 'Healthcare'
        },
        {
            'title': 'Civil Engineer',
            'description': '''Join our engineering team to work on exciting infrastructure projects across Nepal. We're looking for a motivated civil engineer with experience in project management.''',
            'requirements': '''• Bachelor's degree in Civil Engineering
• 3+ years of experience in construction/infrastructure
• Proficiency in AutoCAD, Revit
• Knowledge of construction codes and regulations
• Strong project management skills
• Valid engineering license preferred''',
            'responsibilities': '''• Design and plan construction projects
• Supervise construction activities
• Prepare technical drawings and specifications
• Ensure compliance with safety regulations
• Coordinate with contractors and stakeholders
• Manage project timelines and budgets''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'mid_level',
            'salary_min': 70000,
            'salary_max': 100000,
            'industry_match': 'Construction & Engineering'
        },
        {
            'title': 'Financial Analyst',
            'description': '''We are seeking a detail-oriented Financial Analyst to join our finance team and support data-driven decision making.''',
            'requirements': '''• Bachelor's degree in Finance, Accounting, or Economics
• 2+ years of financial analysis experience
• Proficiency in Excel, financial modeling
• Knowledge of financial regulations
• Strong analytical and communication skills
• CFA or similar certification preferred''',
            'responsibilities': '''• Prepare financial reports and analysis
• Develop financial models and forecasts
• Monitor market trends and economic indicators
• Support budgeting and planning processes
• Present findings to management
• Ensure compliance with financial regulations''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'entry_level',
            'salary_min': 50000,
            'salary_max': 75000,
            'industry_match': 'Banking & Finance'
        },
        {
            'title': 'Secondary School Teacher - Science',
            'description': '''We are looking for an enthusiastic Science Teacher to inspire and educate our secondary school students in Physics, Chemistry, and Biology.''',
            'requirements': '''• Master's degree in Science Education or related field
• Valid teaching license
• 3+ years of teaching experience
• Strong subject knowledge in Sciences
• Excellent communication and classroom management skills
• Passion for education and student development''',
            'responsibilities': '''• Plan and deliver engaging science lessons
• Assess student progress and provide feedback
• Develop curriculum and learning materials
• Participate in school activities and events
• Communicate with parents and colleagues
• Stay updated with educational best practices''',
            'location': 'Pokhara, Nepal',
            'job_type': 'full_time',
            'experience_level': 'mid_level',
            'salary_min': 45000,
            'salary_max': 65000,
            'industry_match': 'Education'
        },
        {
            'title': 'HR Manager',
            'description': '''Lead our human resources department and drive strategic HR initiatives to support our growing organization.''',
            'requirements': '''• Master's degree in HR or related field
• 5+ years of HR management experience
• Knowledge of labor laws and regulations
• Experience with HRIS systems
• Strong leadership and interpersonal skills
• Professional HR certification preferred''',
            'responsibilities': '''• Develop and implement HR policies
• Oversee recruitment and selection processes
• Manage employee relations and performance
• Coordinate training and development programs
• Ensure compliance with labor laws
• Support organizational change initiatives''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'senior_level',
            'salary_min': 90000,
            'salary_max': 130000,
            'industry_match': 'Information Technology'
        },
        {
            'title': 'Graphic Designer',
            'description': '''Join our creative team as a Graphic Designer and bring visual concepts to life for our diverse range of projects.''',
            'requirements': '''• Bachelor's degree in Graphic Design or Fine Arts
• 2+ years of design experience
• Proficiency in Adobe Creative Suite
• Strong portfolio demonstrating design skills
• Understanding of branding and visual identity
• Excellent creativity and attention to detail''',
            'responsibilities': '''• Create visual designs for digital and print media
• Develop branding materials and marketing collateral
• Collaborate with marketing and development teams
• Ensure brand consistency across all materials
• Present design concepts to clients
• Stay updated with design trends and tools''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'entry_level',
            'salary_min': 35000,
            'salary_max': 55000,
            'industry_match': 'Digital Marketing'
        },
        {
            'title': 'Customer Service Representative',
            'description': '''Provide excellent customer service and support to our valued clients through various communication channels.''',
            'requirements': '''• Bachelor's degree or equivalent experience
• 1+ years of customer service experience
• Excellent communication skills in English and Nepali
• Basic computer skills
• Problem-solving abilities
• Patience and empathy in customer interactions''',
            'responsibilities': '''• Handle customer inquiries via phone, email, and chat
• Resolve customer complaints and issues
• Process orders and maintain customer records
• Provide product information and support
• Escalate complex issues to supervisors
• Maintain high customer satisfaction standards''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'entry_level',
            'salary_min': 25000,
            'salary_max': 40000,
            'industry_match': 'Information Technology'
        },
        {
            'title': 'Project Manager',
            'description': '''Lead cross-functional teams and manage complex projects from initiation to completion in our growing organization.''',
            'requirements': '''• Bachelor's degree in Engineering or Business
• 4+ years of project management experience
• PMP certification preferred
• Experience with project management tools
• Strong leadership and communication skills
• Ability to manage multiple projects simultaneously''',
            'responsibilities': '''• Plan and execute project deliverables
• Coordinate with stakeholders and team members
• Monitor project progress and timelines
• Manage project budgets and resources
• Identify and mitigate project risks
• Prepare and present project reports''',
            'location': 'Kathmandu, Nepal',
            'job_type': 'full_time',
            'experience_level': 'senior_level',
            'salary_min': 85000,
            'salary_max': 120000,
            'industry_match': 'Construction & Engineering'
        }
    ]
    
    print("Creating jobs...")
    created_jobs = []
    
    for job_data in jobs_data:
        # Find matching company by industry
        matching_companies = [c for c in companies if c.industry == job_data['industry_match']]
        if not matching_companies:
            matching_companies = companies  # Fallback to any company
        
        company = random.choice(matching_companies)
        
        # Find matching category
        matching_categories = [c for c in categories if job_data['industry_match'].lower() in c.name.lower()]
        if not matching_categories:
            category = random.choice(categories) if categories else None
        else:
            category = matching_categories[0]
        
        # Create job
        job = Job.objects.create(
            title=job_data['title'],
            description=job_data['description'],
            requirements=job_data['requirements'],
            responsibilities=job_data['responsibilities'],
            location=job_data['location'],
            job_type=job_data['job_type'],
            experience_level=job_data['experience_level'],
            salary_min=job_data['salary_min'],
            salary_max=job_data['salary_max'],
            application_deadline=timezone.now().date() + timedelta(days=random.randint(15, 60)),
            company=company,
            category=category,
            posted_by=company.user_profile.user,
            is_active=True
        )
        
        created_jobs.append(job)
        print(f"  ✓ Created job: {job_data['title']} at {company.company_name}")
    
    return created_jobs

def create_job_applications():
    """Create sample job applications"""
    jobs = list(Job.objects.all())
    job_seekers = list(JobSeekerProfile.objects.all())
    
    if not jobs or not job_seekers:
        print("No jobs or job seekers found! Please create them first.")
        return
    
    print("Creating job applications...")
    
    statuses = ['pending', 'reviewed', 'shortlisted', 'interview', 'rejected', 'hired']
    
    # Create random applications
    for _ in range(25):
        job = random.choice(jobs)
        job_seeker = random.choice(job_seekers)
        
        # Check if application already exists
        if JobApplication.objects.filter(job=job, applicant=job_seeker).exists():
            continue
        
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.title} position at {job.company.company_name}. With my background in {job_seeker.skills.split(',')[0].strip()}, I am confident that I would be a valuable addition to your team.

My {job_seeker.experience_years} years of experience in {job_seeker.skills.split(',')[0].strip()} has equipped me with the skills necessary to excel in this role. I am particularly drawn to your company because of its reputation for innovation and commitment to excellence.

I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my skills and passion align with your needs.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
{job_seeker.first_name} {job_seeker.last_name}"""
        
        # Create application
        application = JobApplication.objects.create(
            job=job,
            applicant=job_seeker,
            cover_letter=cover_letter,
            status=random.choice(statuses),
            applied_at=timezone.now() - timedelta(days=random.randint(1, 30))
        )
        
        print(f"  ✓ Created application: {job_seeker.first_name} {job_seeker.last_name} → {job.title}")

def main():
    """Main function to populate all data"""
    print("🚀 Starting database population...")
    print("=" * 50)
    
    try:
        # Create data in order
        create_job_categories()
        print()
        
        companies = create_companies()
        print()
        
        job_seekers = create_job_seekers()
        print()
        
        jobs = create_jobs()
        print()
        
        create_job_applications()
        print()
        
        print("=" * 50)
        print("✅ Database population completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Job Categories: {JobCategory.objects.count()}")
        print(f"   • Companies: {CompanyProfile.objects.count()}")
        print(f"   • Job Seekers: {JobSeekerProfile.objects.count()}")
        print(f"   • Jobs: {Job.objects.count()}")
        print(f"   • Applications: {JobApplication.objects.count()}")
        print()
        print("🔐 Default login credentials:")
        print("   Companies: username/company123")
        print("   Job Seekers: username/jobseeker123")
        print("   Admin: admin/admin123 (if created)")
        
    except Exception as e:
        print(f"❌ Error during population: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 