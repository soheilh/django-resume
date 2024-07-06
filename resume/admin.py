from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
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
    list_display = ('degree', 'major', 'institution', 'start_date', 'end_date',)
    list_filter = ('degree', 'start_date', 'end_date',)
    search_fields = ('major', 'institution_name', 'thesis',)
    date_hierarchy = 'start_date'

class LinkAdmin(GenericTabularInline):
    model = Link
    extra = 1

@admin.register(JournalPublication)
class JournalPublicationAdmin(admin.ModelAdmin):
    inlines = [ LinkAdmin ]

@admin.register(ConferencePublication)
class ConferencePublicationAdmin(admin.ModelAdmin):
    inlines = [ LinkAdmin ]

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
