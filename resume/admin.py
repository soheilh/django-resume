from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bio)
admin.site.register(University)
admin.site.register(Advisor)
admin.site.register(Education)
admin.site.register(Publication)
admin.site.register(PublicationLink)