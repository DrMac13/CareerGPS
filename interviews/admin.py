# interviews/admin.py

from django.contrib import admin
from .models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
    InterviewFeedback
)

admin.site.register(InterviewSession)
admin.site.register(InterviewQuestion)
admin.site.register(InterviewResponse)
admin.site.register(InterviewFeedback)