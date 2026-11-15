from django.urls import path

from . import views

app_name = "audit"

urlpatterns = [
    path("asset/<int:pk>/", views.asset_history, name="asset"),
    path("audit-log/", views.audit_search, name="search"),
]
