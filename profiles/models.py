from django.db import models
from django.contrib.auth.models import User


class Institution(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DegreeProgram(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    degree_program = models.ForeignKey(
        DegreeProgram,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    cv_file = models.FileField(
        upload_to="cvs/",
        blank=True,
        null=True
    )

    cv_text = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username
    
class UserEducation(models.Model):

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    institution_name = models.CharField(
        max_length=200
    )

    qualification_name = models.CharField(
        max_length=200
    )

    field_of_study = models.CharField(
        max_length=200,
        blank=True
    )

    start_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    end_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    source = models.CharField(
        max_length=50,
        default="CV"
    )

    def __str__(self):
        return f"{self.qualification_name} - {self.institution_name}"


class UserSkill(models.Model):

    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default='Beginner'
    )

    years_experience = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.skill.name}"

class UserInterest(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    interest = models.ForeignKey(
        Interest,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.interest.name}"
