from django.contrib import admin
from .models import (
    Company,
    Opportunity,
    OpportunitySkill,
    Bookmark,
    Application
)

admin.site.register(Company)
admin.site.register(Opportunity)
admin.site.register(OpportunitySkill)
admin.site.register(Bookmark)
admin.site.register(Application)