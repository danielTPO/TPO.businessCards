"""QR code generation service.

Produces a square PIL Image containing a QR code.  The image is always RGBA
so it can be composited cleanly over both light and dark backgrounds.
"""

from __future__ import annotations

import logging
from typing import Optional

from PIL import Image

log = logging.getLogger(__name__)


class QRService:
    """Stateless QR code generator.

    All methods are class-level so the service requires no instantiation.

    Example::

        img = QRService.generate("https://example.com", size_px=150)
    """

    @classmethod
    def generate(
        cls,
        url: str,
        size_px: int = 150,
        bg: tuple[int, int, int] = (255, 255, 255),
        fg: tuple[int, int, int] = (26, 26, 26),
    ) -> Optional[Image.Image]:
        """Generate a QR code PIL image.

        Args:
            url: The data to encode (typically a URL).
            size_px: Target output size in pixels (the image is always square).
            bg: Background colour as an (R, G, B) tuple.
            fg: Foreground (module) colour as an (R, G, B) tuple.

        Returns:
            A square RGBA ``PIL.Image.Image``, or ``None`` if the ``qrcode``
            library is not installed.
        """
        try:
            import qrcode  # type: ignore[import]
            from qrcode.image.pil import PilImage  # type: ignore[import]
        except ImportError:
            log.warning("qrcode library not installed — QR code will be omitted")
            return None

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img: Image.Image = qr.make_image(
            fill_color=fg,
            back_color=bg,
        ).get_image()

        # Resize to the requested output size with high-quality resampling
        img = img.resize((size_px, size_px), Image.NEAREST).convert("RGBA")
        return img

    @classmethod
    def generate_vcard_url(cls, contact_fields: dict[str, str]) -> str:
        """Build a minimal vCard 3.0 string suitable for embedding in a QR code.

        Args:
            contact_fields: Dict with keys matching :class:`~bizcard.models.contact.Contact`
                field names.

        Returns:
            A vCard 3.0 formatted string.
        """
        lines = ["BEGIN:VCARD", "VERSION:3.0"]
        if name := contact_fields.get("name"):
            lines.append(f"FN:{name}")
        if title := contact_fields.get("title"):
            lines.append(f"TITLE:{title}")
        if company := contact_fields.get("company"):
            lines.append(f"ORG:{company}")
        if email := contact_fields.get("email"):
            lines.append(f"EMAIL:{email}")
        if phone := contact_fields.get("phone"):
            lines.append(f"TEL:{phone}")
        if website := contact_fields.get("website"):
            url = website if website.startswith("http") else f"https://{website}"
            lines.append(f"URL:{url}")
        lines.append("END:VCARD")
        return "\r\n".join(lines)
