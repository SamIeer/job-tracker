from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'position', 'application_date', 'status', 'user')
    list_filter = ('status', 'application_date')
    search_fields = ('company_name', 'position')

admin.site.register(Job, JobAdmin)

