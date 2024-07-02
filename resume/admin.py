from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bio)
admin.site.register(University)
admin.site.register(Advisor)
admin.site.register(Author)
admin.site.register(LinkType)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'major', 'university', 'start', 'end',)
    list_filter = ('degree', 'start', 'end',)
    search_fields = ('major', 'university_title', 'thesis',)
    date_hierarchy = 'start'

class PublicationLinkAdmin(admin.StackedInline):
    model = PublicationLink

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    inlines = [ PublicationLinkAdmin ]

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('get_title_snippet', 'start_date', 'end_date', 'date_display')