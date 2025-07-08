# Elevate Workforce Solutions

A comprehensive Django-based job portal designed specifically for Nepal's employment market. This platform connects job seekers with top employers, featuring a modern, professional interface and advanced job matching capabilities.

## 🚀 Features

### For Job Seekers
- **User Registration & Authentication** - Secure account creation with profile setup
- **Advanced Job Search** - Filter by title, location, category, salary, experience level
- **Application Tracking** - Monitor application status (Pending, Interview, Hired, Rejected)
- **Profile Management** - Upload resume, showcase skills and experience
- **Personalized Dashboard** - View applications, statistics, and quick actions

### For Employers
- **Company Profiles** - Showcase company information and culture
- **Job Posting Management** - Create, edit, and manage job listings
- **Application Management** - Review and process candidate applications
- **Analytics Dashboard** - Track job performance and application metrics

### Platform Features
- **Responsive Design** - Professional UI with navy blue and gold corporate theme
- **Advanced Filtering** - Multi-criteria job search and sorting options
- **Real-time Updates** - Application status notifications
- **Secure File Upload** - Resume and document management
- **SEO Optimized** - Search engine friendly URLs and meta tags

## 🛠️ Technology Stack

- **Backend:** Django 4.2+
- **Database:** SQLite (development) / PostgreSQL (production ready)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication:** Django's built-in authentication system
- **File Handling:** Django's file upload system
- **Form Handling:** Django Crispy Forms

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/elevate-workforce-solutions.git
   cd elevate-workforce-solutions
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python populate_data.py
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## 📱 Usage

### For Job Seekers
1. Register an account and select "Job Seeker"
2. Complete your profile with skills, experience, and resume
3. Browse jobs using advanced filters
4. Apply to relevant positions
5. Track application status in your dashboard

### For Employers
1. Register an account and select "Company"
2. Set up your company profile
3. Post job listings with detailed requirements
4. Review and manage applications
5. Update application statuses

## 🏗️ Project Structure

```
elevate_workforce/
├── accounts/              # User authentication and profiles
├── jobs/                  # Job listings and applications
├── elevate_workforce/     # Main project settings
├── static/               # CSS, JavaScript, images
├── templates/            # HTML templates
├── media/               # User uploaded files
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── populate_data.py    # Sample data script
```

## 🎨 Design Features

- **Corporate Professional Theme** - Navy blue (#1e3a8a) and gold (#d97706) color scheme
- **Modern UI Components** - Enhanced forms, interactive elements, and smooth animations
- **Responsive Layout** - Mobile-first design approach
- **Accessibility** - WCAG compliant with proper contrast ratios
- **Loading States** - Visual feedback for user interactions

## 📊 Database Schema

### Main Models
- **User** - Django's built-in user model
- **UserProfile** - Extended user information
- **JobSeekerProfile** - Job seeker specific data
- **CompanyProfile** - Company information and details
- **Job** - Job listings with requirements and descriptions
- **JobApplication** - Application tracking and status management

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Static Files
```bash
python manage.py collectstatic
```

## 🚀 Deployment

### For Production
1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend for notifications
5. Use environment variables for sensitive data

### Recommended Hosting
- **Heroku** - Easy deployment with buildpacks
- **DigitalOcean** - App Platform or Droplets
- **AWS** - Elastic Beanstalk or EC2
- **PythonAnywhere** - Simple Django hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Pratik** - [Your GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Font Awesome for icons
- Nepal's job market insights and requirements

## 📞 Support

For support, email your-email@example.com or create an issue in this repository.

---

**Made with ❤️ for Nepal's workforce development** 