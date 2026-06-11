from django.db import models
from django.contrib.auth.models import User


class InterviewSession(models.Model):

    ROLE_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('Business Analyst', 'Business Analyst'),
        ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    overall_score = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class InterviewQuestion(models.Model):

    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE
    )

    question_text = models.TextField()

    question_order = models.PositiveIntegerField()

    def __str__(self):
        return self.question_text[:50]


class InterviewResponse(models.Model):

    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        InterviewQuestion,
        on_delete=models.CASCADE
    )

    response_text = models.TextField()

    duration_seconds = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Response {self.id}"


class InterviewFeedback(models.Model):

    response = models.OneToOneField(
        InterviewResponse,
        on_delete=models.CASCADE
    )

    confidence_score = models.FloatField(
        null=True,
        blank=True
    )

    eye_contact_score = models.FloatField(
        null=True,
        blank=True
    )

    star_score = models.FloatField(
        null=True,
        blank=True
    )

    speaking_pace = models.FloatField(
        null=True,
        blank=True
    )

    overall_score = models.FloatField(
        null=True,
        blank=True
    )

    strengths = models.TextField(
        blank=True
    )

    improvements = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Feedback {self.response.id}"