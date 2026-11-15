from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Department, Role, User, UserRole


class UserRoleInline(admin.TabularInline):
    model = UserRole
    fk_name = "user"
    extra = 0
    fields = ("role", "department", "status")


@admin.register(User)
class DawraUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Dawra Campus", {"fields": ("department", "account_status", "locked_until")}),)
    list_display = ("username", "first_name", "last_name", "department", "account_status")
    list_filter = ("department", "account_status")
    inlines = [UserRoleInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "department", "status")
    list_filter = ("role", "department", "status")
