# Generated by Django 4.2.7 on 2025-07-08 05:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("job_seeker", "Job Seeker"), ("company", "Company")],
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        default="profile_pics/default.jpg", upload_to="profile_pics"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobSeekerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "resume",
                    models.FileField(blank=True, null=True, upload_to="resumes/"),
                ),
                (
                    "skills",
                    models.TextField(help_text="Enter skills separated by commas"),
                ),
                ("experience_years", models.IntegerField(default=0)),
                ("education", models.TextField(blank=True, null=True)),
                (
                    "user_profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=200)),
                ("company_description", models.TextField()),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "company_size",
                    models.CharField(
                        choices=[
                            ("1-10", "1-10 employees"),
                            ("11-50", "11-50 employees"),
                            ("51-200", "51-200 employees"),
                            ("201-500", "201-500 employees"),
                            ("501+", "501+ employees"),
                        ],
                        max_length=50,
                    ),
                ),
                ("industry", models.CharField(max_length=100)),
                ("established_year", models.IntegerField(blank=True, null=True)),
                (
                    "user_profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userprofile",
                    ),
                ),
            ],
        ),
    ]
