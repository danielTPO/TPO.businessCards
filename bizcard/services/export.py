"""Export service — writes rendered artefacts to disk.

:class:`ExportService` is the only component that performs file I/O (aside from
reading input data).  All rendering happens in memory via
:class:`~bizcard.services.render.RenderService`; the export service simply
receives bytes or Pillow Images and writes them under a predictable naming scheme.

Naming convention:
    ``{output_dir}/{lastname}_{firstname}_businesscard.pdf``
    ``{output_dir}/{lastname}_{firstname}_businesscard.png``

Contact sheets (multi-card proof PDFs) are written as:
    ``{output_dir}/contact_sheet.pdf``
"""

from __future__ import annotations

import io
import logging
import math
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from PIL import Image

from bizcard.config import settings

if TYPE_CHECKING:
    from bizcard.models.card import CardSpec
    from bizcard.models.contact import Contact
    from bizcard.services.render import RenderService
    from bizcard.templates.base import BaseTemplate

log = logging.getLogger(__name__)


class ExportService:
    """Writes PDF, PNG, and JPEG artefacts to the output directory.

    Args:
        output_dir: Directory where output files are written.  Created if it
            does not exist.
        renderer: A :class:`~bizcard.services.render.RenderService` instance.
            If ``None``, a default-configured service is created lazily.

    Example::

        exporter = ExportService(output_dir=Path("./cards"))
        exporter.export_pdf(pdf_bytes, contact)
        exporter.export_png(image, contact)
    """

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        renderer: "Optional[RenderService]" = None,
    ) -> None:
        self._output_dir = output_dir or settings.output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._renderer = renderer

    @property
    def renderer(self) -> "RenderService":
        if self._renderer is None:
            from bizcard.services.render import RenderService
            self._renderer = RenderService()
        return self._renderer

    # ------------------------------------------------------------------
    # Atomic export methods
    # ------------------------------------------------------------------

    def export_pdf(self, pdf_bytes: bytes, contact: "Contact") -> Path:
        """Write PDF bytes to ``{output_dir}/{stem}_businesscard.pdf``.

        Args:
            pdf_bytes: PDF content as bytes.
            contact: Contact record — used to derive the filename.

        Returns:
            The path of the written file.
        """
        dest = self._output_dir / f"{contact.output_filename_stem}_businesscard.pdf"
        dest.write_bytes(pdf_bytes)
        log.info("Wrote PDF → %s", dest)
        return dest

    def export_png(
        self,
        image: Image.Image,
        contact: "Contact",
        dpi: int = 150,
    ) -> Path:
        """Write a Pillow Image to ``{output_dir}/{stem}_businesscard.png``.

        Args:
            image: The card image to write.
            contact: Contact record — used to derive the filename.
            dpi: DPI metadata embedded in the PNG header.

        Returns:
            The path of the written file.
        """
        dest = self._output_dir / f"{contact.output_filename_stem}_businesscard.png"
        image.convert("RGB").save(str(dest), format="PNG", dpi=(dpi, dpi))
        log.info("Wrote PNG → %s", dest)
        return dest

    def export_jpeg(
        self,
        image: Image.Image,
        contact: "Contact",
        dpi: int = 150,
        quality: int = 92,
    ) -> Path:
        """Write a Pillow Image to ``{output_dir}/{stem}_businesscard.jpg``."""
        dest = self._output_dir / f"{contact.output_filename_stem}_businesscard.jpg"
        image.convert("RGB").save(str(dest), format="JPEG", dpi=(dpi, dpi), quality=quality)
        log.info("Wrote JPEG → %s", dest)
        return dest

    # ------------------------------------------------------------------
    # High-level convenience methods
    # ------------------------------------------------------------------

    def generate_card(
        self,
        contact: "Contact",
        template: "BaseTemplate",
        *,
        pdf: bool = True,
        png: bool = False,
        jpeg: bool = False,
        include_back: bool = False,
        preview_dpi: int = 150,
    ) -> dict[str, Path]:
        """Render and export a single contact in all requested formats.

        Args:
            contact: The contact record.
            template: The card template to apply.
            pdf: Write a PDF file.
            png: Write a PNG preview.
            jpeg: Write a JPEG preview.
            include_back: Include the back face.
            preview_dpi: DPI for PNG/JPEG output.

        Returns:
            Dict mapping format names (``"pdf"``, ``"png"``, ``"jpeg"``) to
            the paths of the written files.
        """
        paths: dict[str, Path] = {}

        if pdf:
            pdf_bytes = self.renderer.render_pdf(contact, template, include_back=include_back)
            paths["pdf"] = self.export_pdf(pdf_bytes, contact)

        if png or jpeg:
            img = self.renderer.render_image(contact, template, dpi=preview_dpi, include_back=include_back)
            if png:
                paths["png"] = self.export_png(img, contact, dpi=preview_dpi)
            if jpeg:
                paths["jpeg"] = self.export_jpeg(img, contact, dpi=preview_dpi)

        return paths

    def generate_batch(
        self,
        contacts: list["Contact"],
        template: "BaseTemplate",
        *,
        pdf: bool = True,
        png: bool = False,
        include_back: bool = False,
        preview_dpi: int = 150,
    ) -> list[dict[str, Path]]:
        """Render and export a batch of contacts.

        Args:
            contacts: List of contact records.
            template: The card template to apply.
            pdf: Write PDF files.
            png: Write PNG preview files.
            include_back: Include the back face.
            preview_dpi: DPI for PNG output.

        Returns:
            List of path-dicts, one per contact (same order as input).
        """
        results = []
        for i, contact in enumerate(contacts, start=1):
            log.info("[%d/%d] Generating card for %s", i, len(contacts), contact.name)
            paths = self.generate_card(
                contact, template,
                pdf=pdf, png=png, include_back=include_back,
                preview_dpi=preview_dpi,
            )
            results.append(paths)
        return results

    # ------------------------------------------------------------------
    # Contact sheet
    # ------------------------------------------------------------------

    def generate_contact_sheet(
        self,
        contacts: list["Contact"],
        template: "BaseTemplate",
        output_name: str = "contact_sheet.pdf",
        cards_per_row: int = 2,
        preview_dpi: int = 150,
    ) -> Path:
        """Generate a single proof PDF with all cards laid out on pages.

        Cards are arranged in a grid (``cards_per_row`` columns) on US Letter
        pages (8.5 × 11 inches).  Each card appears at its native size with a
        small margin between cards.

        Args:
            contacts: List of contact records to include.
            template: The card template to apply.
            output_name: Filename for the contact sheet PDF.
            cards_per_row: Number of card columns per page.
            preview_dpi: DPI for rendering individual card images.

        Returns:
            Path to the written contact sheet PDF.
        """
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import LETTER

        dest = self._output_dir / output_name
        buf = io.BytesIO()

        PAGE_W, PAGE_H = LETTER  # 612 × 792 pt

        spec = self.renderer._spec
        card_w_pt = spec.width_pt
        card_h_pt = spec.height_pt
        gutter = 14.0  # points between cards

        cols = cards_per_row
        rows_per_page = math.floor(
            (PAGE_H - gutter) / (card_h_pt + gutter)
        )

        c = rl_canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
        c.setTitle("Business Card Contact Sheet")

        card_idx = 0
        total = len(contacts)

        while card_idx < total:
            page_card_idx = 0
            for row in range(rows_per_page):
                for col in range(cols):
                    if card_idx >= total:
                        break
                    contact = contacts[card_idx]
                    card_idx += 1

                    img = self.renderer.render_image(contact, template, dpi=preview_dpi)
                    img_rgb = img.convert("RGB")

                    buf_card = io.BytesIO()
                    img_rgb.save(buf_card, format="PNG")
                    buf_card.seek(0)

                    x = gutter + col * (card_w_pt + gutter)
                    y_top = PAGE_H - gutter - (row + 1) * card_h_pt - row * gutter
                    from reportlab.lib.utils import ImageReader
                    c.drawImage(ImageReader(buf_card), x, y_top, card_w_pt, card_h_pt)

                    # Label beneath each card
                    c.setFont("Helvetica", 7)
                    c.setFillColorRGB(0.4, 0.4, 0.4)
                    c.drawString(x, y_top - 8, contact.name)

                    page_card_idx += 1

            c.showPage()

        c.save()
        buf.seek(0)
        dest.write_bytes(buf.read())
        log.info("Wrote contact sheet (%d cards) → %s", total, dest)
        return dest
