from django.urls import path

from . import views

app_name = "ai"

urlpatterns = [
    path("assets/<int:pk>/classify/", views.classify_asset, name="classify"),
    path("suggestions/<int:pk>/respond/", views.classification_respond, name="respond"),
    path("requests/<int:pk>/matches/", views.request_matches, name="matches"),
    path("matches/<int:pk>/choose/", views.choose_match, name="choose"),
    path("matches/<int:pk>/reject/", views.reject_match, name="reject"),
    path("report/draft/", views.report_draft, name="report_draft"),
    path("report/<int:pk>/publish/", views.report_publish, name="report_publish"),
]
