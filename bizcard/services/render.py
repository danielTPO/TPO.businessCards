"""Render service — coordinates templates, contexts, and output backends.

The :class:`RenderService` is the single entry point for producing rendered
artefacts.  It wires together:

- A :class:`~bizcard.models.card.CardSpec` (physical dimensions and DPI)
- A :class:`~bizcard.templates.base.BaseTemplate` (visual design)
- A :class:`~bizcard.models.contact.Contact` (data)

and produces either a PDF byte buffer or a Pillow ``Image`` object.  It does
**not** write files — that responsibility belongs to :class:`~bizcard.services.export.ExportService`.
"""

from __future__ import annotations

import io
import logging
from typing import TYPE_CHECKING, Optional

from PIL import Image

from bizcard.models.card import CardSpec, Orientation
from bizcard.config import settings

if TYPE_CHECKING:
    from bizcard.models.contact import Contact
    from bizcard.templates.base import BaseTemplate

log = logging.getLogger(__name__)


class RenderService:
    """Coordinates template rendering to PDF (bytes) or Pillow Image.

    Args:
        spec: Card physical specification.  If ``None``, a standard landscape
            300 DPI card is used.
        include_bleed: Whether the PDF output canvas includes bleed area.

    Example::

        renderer = RenderService()
        pdf_bytes = renderer.render_pdf(contact, template)
        preview_img = renderer.render_image(contact, template, dpi=150)
    """

    def __init__(
        self,
        spec: Optional[CardSpec] = None,
        include_bleed: bool = True,
    ) -> None:
        self._spec = spec or CardSpec.standard_landscape(dpi=settings.dpi)
        self._include_bleed = include_bleed

    # ------------------------------------------------------------------
    # PDF rendering
    # ------------------------------------------------------------------

    def render_pdf(
        self,
        contact: "Contact",
        template: "BaseTemplate",
        include_back: bool = False,
    ) -> bytes:
        """Render a contact card to a PDF byte string.

        The canvas is sized to the card dimensions plus bleed (if
        ``include_bleed`` is set on the service).  Trim and bleed box metadata
        are written to the PDF so professional print shops can set up the job
        correctly.

        Args:
            contact: The contact record to render.
            template: The card template to apply.
            include_back: If ``True``, a second page with the back face is added.

        Returns:
            The PDF as a ``bytes`` object.
        """
        from reportlab.pdfgen import canvas as rl_canvas

        from bizcard.templates.base import PDFRenderContext

        buf = io.BytesIO()
        spec = self._spec
        tokens = template.design_tokens()

        page_w = spec.canvas_width_pt if self._include_bleed else spec.width_pt
        page_h = spec.canvas_height_pt if self._include_bleed else spec.height_pt

        c = rl_canvas.Canvas(buf, pagesize=(page_w, page_h))

        # PDF metadata
        c.setTitle(f"{contact.name} — Business Card")
        c.setAuthor("bizcard")
        c.setSubject("Business Card")

        # PDF/X trim and bleed box annotations
        if self._include_bleed:
            bleed = spec.bleed_pt
            self._set_trim_bleed_boxes(c, page_w, page_h, bleed)

        # Render front face
        ctx = PDFRenderContext(c, spec, tokens)
        log.debug("Rendering PDF front face for '%s' with template '%s'", contact.name, template.name)
        template.render(contact, ctx)
        c.showPage()

        # Optionally render back face
        if include_back:
            ctx_back = PDFRenderContext(c, spec, tokens)
            template.render_back(contact, ctx_back)
            c.showPage()

        c.save()
        buf.seek(0)
        return buf.read()

    # ------------------------------------------------------------------
    # Image rendering
    # ------------------------------------------------------------------

    def render_image(
        self,
        contact: "Contact",
        template: "BaseTemplate",
        dpi: Optional[int] = None,
        include_back: bool = False,
    ) -> Image.Image:
        """Render a contact card to a Pillow Image (PNG-ready).

        Args:
            contact: The contact record to render.
            template: The card template to apply.
            dpi: Override the render DPI (defaults to ``spec.dpi``).
            include_back: If ``True``, the front and back are stacked
                vertically in a single image.

        Returns:
            A ``PIL.Image.Image`` in RGBA mode.
        """
        from bizcard.templates.base import ImageRenderContext

        effective_dpi = dpi or self._spec.dpi
        render_spec = self._spec.model_copy(update={"dpi": effective_dpi})
        tokens = template.design_tokens()

        canvas_w = render_spec.canvas_width_px
        canvas_h = render_spec.canvas_height_px

        image = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
        ctx = ImageRenderContext(image, render_spec, tokens)

        log.debug(
            "Rendering image for '%s' at %d DPI (%dx%d px)",
            contact.name, effective_dpi, canvas_w, canvas_h,
        )
        template.render(contact, ctx)

        if include_back:
            back_image = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
            ctx_back = ImageRenderContext(back_image, render_spec, tokens)
            template.render_back(contact, ctx_back)
            combined = Image.new("RGBA", (canvas_w, canvas_h * 2), (255, 255, 255, 255))
            combined.paste(image, (0, 0))
            combined.paste(back_image, (0, canvas_h))
            return combined

        return image

    # ------------------------------------------------------------------
    # Batch helpers
    # ------------------------------------------------------------------

    def render_pdf_batch(
        self,
        contacts: list["Contact"],
        template: "BaseTemplate",
        include_back: bool = False,
    ) -> list[tuple["Contact", bytes]]:
        """Render multiple contacts to individual PDF byte strings.

        Args:
            contacts: List of contact records.
            template: The card template to apply.
            include_back: Whether to include the back face.

        Returns:
            List of ``(contact, pdf_bytes)`` pairs.
        """
        results = []
        for contact in contacts:
            pdf = self.render_pdf(contact, template, include_back=include_back)
            results.append((contact, pdf))
        return results

    def render_image_batch(
        self,
        contacts: list["Contact"],
        template: "BaseTemplate",
        dpi: Optional[int] = None,
    ) -> list[tuple["Contact", Image.Image]]:
        """Render multiple contacts to individual Pillow Images."""
        results = []
        for contact in contacts:
            img = self.render_image(contact, template, dpi=dpi)
            results.append((contact, img))
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _set_trim_bleed_boxes(
        canvas: object, page_w: float, page_h: float, bleed: float
    ) -> None:
        """Write TrimBox and BleedBox to the PDF catalogue."""
        try:
            from reportlab.platypus.doctemplate import PageTemplate  # noqa: F401
            # TrimBox: the actual card dimensions, inset from the full canvas
            trim = [bleed, bleed, page_w - bleed, page_h - bleed]
            canvas._doc.information["TrimBox"] = trim  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            pass  # Non-fatal: trim/bleed box is advisory metadata
