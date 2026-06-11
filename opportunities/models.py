from django.db import models
from django.contrib.auth.models import User
from profiles.models import Skill


class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Opportunity(models.Model):

    OPPORTUNITY_TYPES = [
        ('Job', 'Job'),
        ('Internship', 'Internship'),
        ('Graduate Programme', 'Graduate Programme'),
        ('Learnership', 'Learnership'),
        ('Scholarship', 'Scholarship'),
        ('Bursary', 'Bursary'),
    ]

    EXPERIENCE_LEVELS = [
        ('Entry', 'Entry'),
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]

    title = models.CharField(max_length=255)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    opportunity_type = models.CharField(
        max_length=30,
        choices=OPPORTUNITY_TYPES
    )

    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        default='Entry'
    )

    description = models.TextField()

    location = models.CharField(max_length=200)

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    application_url = models.URLField()

    source = models.CharField(
        max_length=100,
        blank=True
    )

    date_posted = models.DateTimeField(
        auto_now_add=True
    )

    closing_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


class OpportunitySkill(models.Model):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.opportunity.title} - {self.skill.name}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} bookmarked {self.opportunity.title}"


class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interviewing', 'Interviewing'),
        ('Rejected', 'Rejected'),
        ('Offer', 'Offer'),
        ('Accepted', 'Accepted'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"