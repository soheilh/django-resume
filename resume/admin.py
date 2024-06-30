from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bio)
admin.site.register(University)
admin.site.register(Advisor)
admin.site.register(Author)
admin.site.register(LinkType)

class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'major', 'university', 'start', 'end',)
    list_filter = ('degree', 'start', 'end',)
    search_fields = ('major', 'university_title', 'thesis',)
    date_hierarchy = 'start'

admin.site.register(Education, EducationAdmin)

class PublicationLinkAdmin(admin.StackedInline):
    model = PublicationLink

class PublicationAdmin(admin.ModelAdmin):
    inlines = [ PublicationLinkAdmin ]

admin.site.register(Publication, PublicationAdmin)
