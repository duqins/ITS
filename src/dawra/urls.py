"""Top-level URLs. Each app keeps its own pages in its urls.py."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("assets/", include("assets.urls")),
    path("requests/", include("resource_requests.urls")),
    path("transfers/", include("transfers.urls")),
    path("history/", include("audit.urls")),
    path("notifications/", include("notifications.urls")),
    path("sustainability/", include("sustainability.urls")),
    path("reports/", include("reports.urls")),
    path("ai/", include("ai.urls")),
    path("", include("core.urls")),
]
