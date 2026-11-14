from django.contrib import admin

from .models import AiSuggestion, MatchRecommendation, ModelVersion


@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ("task", "model_name", "version", "active_from")


@admin.register(AiSuggestion)
class AiSuggestionAdmin(admin.ModelAdmin):
    list_display = ("task", "asset", "confidence", "user_response", "created_at")


@admin.register(MatchRecommendation)
class MatchRecommendationAdmin(admin.ModelAdmin):
    list_display = ("request", "rank", "asset", "score", "user_response")
