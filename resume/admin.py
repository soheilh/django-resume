from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bio)
admin.site.register(Institution)
admin.site.register(Advisor)
admin.site.register(Author)
admin.site.register(LinkType)
admin.site.register(Activity)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'major', 'institution', 'start', 'end',)
    list_filter = ('degree', 'start', 'end',)
    search_fields = ('major', 'institution_name', 'thesis',)
    date_hierarchy = 'start'

class PublicationLinkAdmin(admin.TabularInline):
    model = PublicationLink

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    inlines = [ PublicationLinkAdmin ]

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('get_title_snippet', 'start_date', 'end_date', 'date_display')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'research', 'start_date', 'end_date', 'duration')

class SkillInline(admin.TabularInline):
    model = Skill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    inlines = [ SkillInline ]
    list_display = ('name', 'skill_to_str')

    def skill_to_str(self, obj):
        return [skill for skill in obj.skills.all()]
    skill_to_str.short_description = 'skills'
