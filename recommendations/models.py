from django.db import models
from django.contrib.auth.models import User
from opportunities.models import Opportunity


class Recommendation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE
    )

    match_score = models.FloatField()

    reasons = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'opportunity')

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"