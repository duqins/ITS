from django.contrib import admin

from .models import ResourceRequest


@admin.register(ResourceRequest)
class ResourceRequestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "requester", "department", "category", "quantity", "status", "required_by")
    list_filter = ("status", "department")
