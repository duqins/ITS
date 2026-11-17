"""Checking and storing the photos and documents of an asset (FR-04.1: up to five JPG or PNG photos of
5 MB each, and PDF documents of 10 MB each).

A photo is opened with Pillow, so only real JPG and PNG images are accepted. It is shrunk first, then turned
upright and saved again as a JPEG of at most 1568 pixels (the size the AI reads best) and as a 480-pixel copy
for lists. Saving it again also drops the camera details, such as the place where the photo was taken.
"""

from io import BytesIO

from django import forms
from django.utils.translation import gettext as _
from PIL import Image, UnidentifiedImageError

MAX_PHOTOS = 5
MAX_DOCUMENTS = 5
PHOTO_MAX_BYTES = 5 * 1024 * 1024
DOCUMENT_MAX_BYTES = 10 * 1024 * 1024
LARGE, SMALL = 1568, 480
# A few megabytes of PNG can hold a picture that needs gigabytes once decoded. The hosting plan has 512 MB,
# so a picture is refused before decoding when it has more pixels than this (a JPEG is first read at a
# reduced scale, so ordinary camera photos stay well below it).
MAX_PIXELS = 16_000_000
# A progressive JPEG needs up to about 7 bytes per pixel of the original while it decodes (measured: 161 MB for
# 24 megapixels), so its original size is limited too. Ordinary phone photos are not progressive.
MAX_PROGRESSIVE_PIXELS = 24_000_000
# EXIF orientation (tag 274) and the turn that makes the photo upright.
UPRIGHT = {2: Image.Transpose.FLIP_LEFT_RIGHT, 3: Image.Transpose.ROTATE_180, 4: Image.Transpose.FLIP_TOP_BOTTOM,
           5: Image.Transpose.TRANSPOSE, 6: Image.Transpose.ROTATE_270, 7: Image.Transpose.TRANSVERSE,
           8: Image.Transpose.ROTATE_90}


def _jpeg(image, longest_side):
    copy = image.copy()
    copy.thumbnail((longest_side, longest_side))
    out = BytesIO()
    copy.save(out, "JPEG", quality=85, optimize=True)
    return out.getvalue()


def _flatten(image):
    """RGB for saving as JPEG; transparent parts become white instead of black."""
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        return background
    return image.convert("RGB")


def read_photo(upload):
    """Return (name, large JPEG, small JPEG) for a JPG or PNG upload, or raise a ValidationError."""
    if upload.size > PHOTO_MAX_BYTES:
        raise forms.ValidationError(_("%(name)s is larger than 5 MB.") % {"name": upload.name})
    try:
        with Image.open(upload) as image:
            # Many phones save a JPEG with a small second picture inside (MPO); the first picture is the photo.
            if image.format not in ("JPEG", "MPO", "PNG"):
                raise forms.ValidationError(_("%(name)s is not a JPG or PNG photo.") % {"name": upload.name})
            width, height = image.size
            # A progressive JPEG keeps data for the whole picture while it is read, whatever the scale.
            if image.info.get("progressive") and width * height > MAX_PROGRESSIVE_PIXELS:
                raise forms.ValidationError(_("%(name)s has too many pixels. Use a photo of at most 16 "
                                              "megapixels.") % {"name": upload.name})
            # JPEG only: read at 1/2, 1/4 or 1/8 scale, but never smaller than the stored copy (panoramas too).
            ratio = min(LARGE / width, LARGE / height, 1)
            image.draft("RGB", (max(1, int(width * ratio)), max(1, int(height * ratio))))
            if image.width * image.height > MAX_PIXELS:
                raise forms.ValidationError(_("%(name)s has too many pixels. Use a photo of at most 16 "
                                              "megapixels.") % {"name": upload.name})
            turn = UPRIGHT.get(image.getexif().get(274))
            image.thumbnail((LARGE, LARGE))  # the only full-size step; everything after works on the small copy
            if turn is not None:
                image = image.transpose(turn)
            image = _flatten(image)
            return upload.name, _jpeg(image, LARGE), _jpeg(image, SMALL)
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError):
        raise forms.ValidationError(_("%(name)s is not a JPG or PNG photo.") % {"name": upload.name})


def read_document(upload):
    """Return (name, PDF bytes) for a PDF upload, or raise a ValidationError."""
    if upload.size > DOCUMENT_MAX_BYTES:
        raise forms.ValidationError(_("%(name)s is larger than 10 MB.") % {"name": upload.name})
    data = upload.read()
    if not data.startswith(b"%PDF-"):
        raise forms.ValidationError(_("%(name)s is not a PDF document.") % {"name": upload.name})
    return upload.name, data
