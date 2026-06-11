from django.db import models
from opportunities.models import Opportunity


class JobSource(models.Model):
    name = models.CharField(max_length=200)

    website = models.URLField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class ScrapeRun(models.Model):

    STATUS_CHOICES = [
        ("Started", "Started"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    source = models.ForeignKey(
        JobSource,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Started"
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    jobs_found = models.PositiveIntegerField(
        default=0
    )

    error_message = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.source.name} - {self.status}"


class ImportedOpportunity(models.Model):

    source = models.ForeignKey(
        JobSource,
        on_delete=models.CASCADE
    )

    external_id = models.CharField(
        max_length=255
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    company_name = models.CharField(
        max_length=255
    )

    source_url = models.URLField()

    last_seen_at = models.DateTimeField(
        auto_now=True
    )

    is_currently_available = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = ("source", "external_id")

    def __str__(self):
        return f"{self.title} - {self.company_name}"