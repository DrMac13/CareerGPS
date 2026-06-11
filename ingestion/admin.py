from django.contrib import admin
from .models import JobSource, ScrapeRun, ImportedOpportunity

admin.site.register(JobSource)
admin.site.register(ScrapeRun)
admin.site.register(ImportedOpportunity)