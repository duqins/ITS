"""Showing an asset's photo: the first photo if there is one, otherwise the line icon of the mockups."""

from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from assets.models import AssetFile
from core.templatetags.dawra_ui import icon

register = template.Library()


@register.simple_tag
def asset_thumb(asset, css="asset-symbol"):
    # A list page can look up every first photo in one query and put it on the asset (assets/views.py search).
    if hasattr(asset, "first_photo"):
        first = asset.first_photo
    else:
        first = AssetFile.objects.filter(asset=asset, kind=AssetFile.Kind.PHOTO).values_list("pk", flat=True).first()
    if first is None:
        return format_html('<div class="{}">{}</div>', css, icon("monitor" if asset.category_id and "IT" in
                                                                  str(asset.category) else "box"))
    url = reverse("assets:file", args=[asset.pk, first]) + "?size=small"
    return format_html('<div class="{} has-photo"><img src="{}" alt="{}" loading="lazy"></div>', css, url,
                       _("Photo of %(name)s") % {"name": asset.name})
