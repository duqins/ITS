"""Template helpers for the Dawra Campus layout (icons, status pills, menu)."""

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html

register = template.Library()

# The 19 line icons of the Phase 4 and 5 mockups (24 x 24 paths).
ICONS = {
    "box": "M21 8 12 3 3 8v9l9 5 9-5V8ZM3 8l9 5 9-5M12 13v9",
    "request": "M8 3h8l4 4v14H4V3h4ZM8 11h8M8 15h6M14 3v5h6",
    "match": "m4 6 3 3 5-5M14 7h6M4 16l3 3 5-5M14 17h6",
    "check": "m5 12 4 4L19 6",
    "approval": "M12 3 3 7v5c0 5 9 9 9 9s9-4 9-9V7l-9-4Zm-4 9 3 3 5-6",
    "transfer": "M3 7h16m-4-4 4 4-4 4M21 17H5m4-4-4 4 4 4",
    "tool": "m14 6 4 4m-7 3-7 7-3-3 7-7M14 3a6 6 0 0 0-7 7l7 7a6 6 0 0 0 7-7l-4 2-4-4 2-5Z",
    "report": "M4 3h16v18H4V3Zm4 13v-4m4 4V8m4 8v-6",
    "chat": "M21 5H3v13h5l4 4v-4h9V5ZM7 10h10M7 14h6",
    "bell": "M18 8a6 6 0 0 0-12 0v7l-2 3h16l-2-3V8ZM10 21h4",
    "spark": "m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z",
    "arrow": "M4 12h16m-6-6 6 6-6 6",
    "info": "M12 8v.1M12 11v6M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0Z",
    "file": "M5 3h9l5 5v13H5V3Zm9 0v5h5M8 13h8M8 17h5",
    "monitor": "M3 4h18v13H3V4Zm9 13v4m-5 0h10",
    "leaf": "M20 3c-8 0-15 2-15 9a7 7 0 0 0 7 7c7 0 8-8 8-16ZM4 21 16 8",
    "clock": "M12 7v6l4 2M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0Z",
    "user": "M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM4 22v-3a8 8 0 0 1 16 0v3",
    "location": "M19 9c0 6-7 12-7 12S5 15 5 9a7 7 0 1 1 14 0Zm-4 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
}


@register.simple_tag
def icon(name):
    return format_html('<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="{}"/></svg>', ICONS.get(name, ICONS["box"]))


@register.filter
def initials(user):
    parts = [user.first_name, user.last_name] if user.first_name else [user.username]
    return "".join(p[0] for p in parts if p).upper()[:2]


@register.inclusion_tag("includes/status.html")
def status_pill(obj):
    return {"label": obj.get_status_display(), "code": obj.status}


# Menu entries: label, icon, URL name, and the actions that show it (empty means every role).
MENU = [
    ("Home", "info", "core:home", ()),
    ("Assets", "box", "assets:list", ("asset.view",)),
    ("Search", "match", "assets:search", ("listing.search",)),
    ("Requests", "request", "resource_requests:list", ("request.submit", "request.approve")),
    ("Approvals", "approval", "transfers:approvals",
     ("request.approve", "listing.publish", "transfer.approve_release", "transfer.approve_receipt",
      "transfer.approve_finance", "transfer.approve_procurement")),
    ("Holds and transfers", "transfer", "transfers:list", ("transfer.view", "hold.confirm")),
    ("Sustainability", "leaf", "sustainability:dashboard", ("dashboard.view",)),
    ("Reports", "report", "reports:index", ("report.view",)),
    ("Audit log", "clock", "audit:search", ("audit.view",)),
]


@register.inclusion_tag("includes/menu.html", takes_context=True)
def main_menu(context):
    request = context["request"]
    role = getattr(request, "active_role", None)
    items = []
    for label, icon_name, url_name, actions in MENU:
        if actions and (role is None or not any(role.allows(a) for a in actions)):
            continue
        try:
            url = reverse(url_name)
        except NoReverseMatch:
            continue  # the section is not built yet
        items.append({"label": label, "icon": icon_name, "url": url, "active": False})
    # Highlight the entry whose address matches the current page most closely.
    matches = [i for i in items if (request.path == i["url"] if i["url"] == "/" else request.path.startswith(i["url"]))]
    if matches:
        max(matches, key=lambda i: len(i["url"]))["active"] = True
    return {"items": items}
