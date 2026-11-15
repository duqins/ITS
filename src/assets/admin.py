from django.contrib import admin

from .models import Asset, Category, FurnitureAsset, ITAsset, Listing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "unit", "emission_factor_low", "emission_factor_high", "is_active")


@admin.register(Asset, ITAsset, FurnitureAsset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "owner_department", "status", "quantity", "available_qty")
    list_filter = ("status", "owner_department", "category")
    search_fields = ("name", "description", "tags")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "quantity", "status", "published_at")
    list_filter = ("status",)
