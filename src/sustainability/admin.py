from django.contrib import admin

from .models import SustainabilityImpact


@admin.register(SustainabilityImpact)
class SustainabilityImpactAdmin(admin.ModelAdmin):
    list_display = ("transfer", "department", "items_diverted", "avoided_purchase_aed", "co2e_low_kg", "co2e_high_kg")
