from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Department, Role, User, UserRole


class ReadOnlyRoles:
    """Roles change only through the Administration page: requested, authorised by another Business
    administrator, then applied (BR-01, BR-02). This site shows them but cannot change them."""

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserRoleInline(ReadOnlyRoles, admin.TabularInline):
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

    def get_fieldsets(self, request, obj=None):
        # A System administrator maintains accounts (FR-01.1) but cannot give anyone extra powers (BR-01).
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser or obj is None:
            return fieldsets
        hidden = {"is_superuser", "is_staff", "groups", "user_permissions"}
        return [(name, {**options, "fields": [f for f in options["fields"] if f not in hidden]})
                for name, options in fieldsets]

    def has_change_permission(self, request, obj=None):
        # Administrator accounts are out of reach for another administrator: no password reset, no deactivation,
        # so nobody can act as a Business administrator or stop role requests being decided (BR-01).
        if obj is not None and not request.user.is_superuser and obj.is_administrator_account():
            return False
        return super().has_change_permission(request, obj)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code",)


@admin.register(UserRole)
class UserRoleAdmin(ReadOnlyRoles, admin.ModelAdmin):
    list_display = ("user", "role", "department", "status")
    list_filter = ("role", "department", "status")
