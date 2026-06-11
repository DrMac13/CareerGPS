from django.contrib import admin
from .models import (
    Institution,
    DegreeProgram,
    Skill,
    Interest,
    UserProfile,
    UserSkill,
    UserInterest
)

admin.site.register(Institution)
admin.site.register(DegreeProgram)
admin.site.register(Skill)
admin.site.register(Interest)
admin.site.register(UserProfile)
admin.site.register(UserSkill)
admin.site.register(UserInterest)