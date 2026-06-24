"""Abstract base template and the RenderContext drawing protocol.

Architecture overview
---------------------
Every card template inherits from :class:`BaseTemplate` and overrides two
methods: :meth:`design_tokens` (returns the palette/typography spec) and
:meth:`render` (draws onto a :class:`RenderContext`).

:class:`RenderContext` is an abstract drawing surface.  Two concrete
implementations exist:

* :class:`PDFRenderContext` — wraps a ReportLab ``canvas.Canvas`` and works in
  points (72 per inch), flipping the Y-axis to match top-left origin.
* :class:`ImageRenderContext` — wraps a Pillow ``ImageDraw.Draw`` and works in
  pixels at the card's target DPI.

Templates never import ReportLab or Pillow directly; they call the context's
methods using point-based coordinates (origin top-left, y increases downward).
This keeps templates renderer-agnostic and makes it easy to add future backends
such as SVG or HTML5 Canvas.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from PIL import Image, ImageDraw, ImageFont

from bizcard.config import FONTS_DIR, DesignTokens, hex_to_rgb

if TYPE_CHECKING:
    from reportlab.pdfgen.canvas import Canvas as RLCanvas

    from bizcard.models.card import CardSpec
    from bizcard.models.contact import Contact

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Font resolution
# ---------------------------------------------------------------------------

_PIL_FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_RL_FONT_REGISTERED: set[str] = set()

# Map logical font names → TTF filenames in assets/fonts/
FONT_FILES: dict[str, str] = {
    "Inter-Bold": "Inter-Bold.ttf",
    "Inter-Regular": "Inter-Regular.ttf",
    "Inter-Medium": "Inter-Medium.ttf",
    "Inter-Light": "Inter-Light.ttf",
    "Inter-SemiBold": "Inter-SemiBold.ttf",
}

# ReportLab built-in fallbacks (no embedding required)
RL_FALLBACK: dict[str, str] = {
    "Inter-Bold": "Helvetica-Bold",
    "Inter-Regular": "Helvetica",
    "Inter-Medium": "Helvetica",
    "Inter-Light": "Helvetica-Oblique",
    "Inter-SemiBold": "Helvetica-Bold",
}


def _resolve_font_path(font_name: str) -> Optional[Path]:
    filename = FONT_FILES.get(font_name)
    if not filename:
        return None
    path = FONTS_DIR / filename
    return path if path.exists() else None


def get_pil_font(font_name: str, size_pt: float, dpi: int) -> ImageFont.FreeTypeFont:
    """Return a Pillow ``FreeTypeFont`` for *font_name* at the given size."""
    size_px = max(1, round(size_pt * dpi / 72.0))
    cache_key = (font_name, size_px)
    if cache_key not in _PIL_FONT_CACHE:
        path = _resolve_font_path(font_name)
        if path:
            _PIL_FONT_CACHE[cache_key] = ImageFont.truetype(str(path), size_px)
        else:
            log.warning("Font '%s' not found in assets/fonts/ — using default", font_name)
            try:
                _PIL_FONT_CACHE[cache_key] = ImageFont.load_default(size=size_px)
            except TypeError:
                _PIL_FONT_CACHE[cache_key] = ImageFont.load_default()
    return _PIL_FONT_CACHE[cache_key]


def register_rl_font(font_name: str) -> str:
    """Register a TTF font with ReportLab and return the registered name.

    Falls back to the nearest built-in Helvetica variant if the TTF file is not
    found in ``assets/fonts/``.
    """
    if font_name in _RL_FONT_REGISTERED:
        return font_name

    path = _resolve_font_path(font_name)
    if path:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            pdfmetrics.registerFont(TTFont(font_name, str(path)))
            _RL_FONT_REGISTERED.add(font_name)
            return font_name
        except Exception as exc:  # noqa: BLE001
            log.warning("Could not register font '%s': %s", font_name, exc)

    fallback = RL_FALLBACK.get(font_name, "Helvetica")
    log.debug("Using ReportLab built-in '%s' as fallback for '%s'", fallback, font_name)
    return fallback


# ---------------------------------------------------------------------------
# RenderContext abstraction
# ---------------------------------------------------------------------------

class RenderContext(ABC):
    """Abstract drawing surface consumed by templates.

    All coordinate arguments are in **points** (1 pt = 1/72 inch) with the
    origin at the **top-left corner of the card trim box** (not including
    bleed).  The Y axis increases **downward**.

    Colours are passed as ``(R, G, B)`` integer tuples in the range 0–255.
    """

    def __init__(self, spec: "CardSpec", tokens: DesignTokens) -> None:
        self._spec = spec
        self._tokens = tokens

    @property
    def card_width_pt(self) -> float:
        """Card width in points, excluding bleed."""
        return self._spec.width_pt

    @property
    def card_height_pt(self) -> float:
        """Card height in points, excluding bleed."""
        return self._spec.height_pt

    # ------------------------------------------------------------------
    # Drawing primitives — must be implemented by subclasses
    # ------------------------------------------------------------------

    @abstractmethod
    def fill_background(self, color: tuple[int, int, int]) -> None:
        """Flood-fill the entire card face (including bleed) with *color*."""

    @abstractmethod
    def draw_rect(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        fill: tuple[int, int, int],
        stroke: Optional[tuple[int, int, int]] = None,
        stroke_width_pt: float = 0.5,
    ) -> None:
        """Draw a filled rectangle with an optional stroke."""

    @abstractmethod
    def draw_line(
        self,
        x1_pt: float,
        y1_pt: float,
        x2_pt: float,
        y2_pt: float,
        color: tuple[int, int, int],
        width_pt: float = 0.5,
    ) -> None:
        """Draw a straight line segment."""

    @abstractmethod
    def draw_text(
        self,
        x_pt: float,
        y_pt: float,
        text: str,
        font_name: str,
        size_pt: float,
        color: tuple[int, int, int],
        align: str = "left",
        max_width_pt: Optional[float] = None,
    ) -> float:
        """Render *text* and return the Y position of the bottom of the text box.

        Args:
            x_pt: Left edge of the text box (or right edge when ``align='right'``).
            y_pt: Top of the text bounding box.
            text: The string to render.
            font_name: Logical font name (e.g. ``"Inter-Bold"``).
            size_pt: Font size in points.
            color: ``(R, G, B)`` fill colour.
            align: ``"left"``, ``"right"``, or ``"center"``.
            max_width_pt: If given, text is clipped or truncated to this width.

        Returns:
            The Y coordinate of the bottom of the rendered text bounding box.
        """

    @abstractmethod
    def draw_image(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        image: Image.Image,
    ) -> None:
        """Composite a PIL Image onto the card at the given position/size."""

    @abstractmethod
    def measure_text_width(self, text: str, font_name: str, size_pt: float) -> float:
        """Return the width in points of *text* rendered in the given font."""


# ---------------------------------------------------------------------------
# Concrete: PDF render context (ReportLab)
# ---------------------------------------------------------------------------

class PDFRenderContext(RenderContext):
    """ReportLab-backed render context.

    Translates top-left–origin point coordinates into ReportLab's bottom-left–
    origin coordinate system and delegates to the underlying ``canvas.Canvas``.
    """

    def __init__(self, canvas: "RLCanvas", spec: "CardSpec", tokens: DesignTokens) -> None:
        super().__init__(spec, tokens)
        self._canvas = canvas
        # The canvas origin is at the bottom-left of the *full page* which
        # includes bleed on all sides.  We offset all coordinates by the bleed
        # so that templates think they are drawing inside a clean trim box.
        self._bleed = spec.bleed_pt
        self._page_height = spec.canvas_height_pt  # total canvas height

    # ------------------------------------------------------------------
    # Coordinate helpers
    # ------------------------------------------------------------------

    def _rl_y(self, y_top_pt: float, box_height_pt: float = 0.0) -> float:
        """Convert top-down Y + box height to ReportLab bottom-left Y."""
        # ReportLab Y = distance from bottom of page to the bottom of the box
        return self._page_height - (y_top_pt + self._bleed + box_height_pt)

    def _rl_x(self, x_pt: float) -> float:
        return x_pt + self._bleed

    def _set_fill(self, color: tuple[int, int, int]) -> None:
        self._canvas.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)

    def _set_stroke(self, color: tuple[int, int, int]) -> None:
        self._canvas.setStrokeColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)

    # ------------------------------------------------------------------
    # RenderContext interface
    # ------------------------------------------------------------------

    def fill_background(self, color: tuple[int, int, int]) -> None:
        self._set_fill(color)
        # Cover the full canvas including bleed
        self._canvas.rect(
            0, 0,
            self._spec.canvas_width_pt,
            self._spec.canvas_height_pt,
            stroke=0, fill=1,
        )

    def draw_rect(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        fill: tuple[int, int, int],
        stroke: Optional[tuple[int, int, int]] = None,
        stroke_width_pt: float = 0.5,
    ) -> None:
        self._set_fill(fill)
        if stroke:
            self._set_stroke(stroke)
            self._canvas.setLineWidth(stroke_width_pt)
        rl_y = self._rl_y(y_pt, h_pt)
        self._canvas.rect(
            self._rl_x(x_pt), rl_y, w_pt, h_pt,
            stroke=1 if stroke else 0,
            fill=1,
        )

    def draw_line(
        self,
        x1_pt: float,
        y1_pt: float,
        x2_pt: float,
        y2_pt: float,
        color: tuple[int, int, int],
        width_pt: float = 0.5,
    ) -> None:
        self._set_stroke(color)
        self._canvas.setLineWidth(width_pt)
        self._canvas.line(
            self._rl_x(x1_pt),
            self._rl_y(y1_pt),
            self._rl_x(x2_pt),
            self._rl_y(y2_pt),
        )

    def draw_text(
        self,
        x_pt: float,
        y_pt: float,
        text: str,
        font_name: str,
        size_pt: float,
        color: tuple[int, int, int],
        align: str = "left",
        max_width_pt: Optional[float] = None,
    ) -> float:
        from reportlab.pdfbase import pdfmetrics

        registered_name = register_rl_font(font_name)
        self._canvas.setFont(registered_name, size_pt)
        self._set_fill(color)

        # Truncate text to max_width if requested
        if max_width_pt:
            text = self._truncate_text_rl(text, registered_name, size_pt, max_width_pt)

        text_width = pdfmetrics.stringWidth(text, registered_name, size_pt)
        ascender = size_pt * 0.75  # approximate cap-height

        if align == "right":
            draw_x = self._rl_x(x_pt) - text_width
        elif align == "center":
            draw_x = self._rl_x(x_pt) - text_width / 2
        else:
            draw_x = self._rl_x(x_pt)

        # y_pt is the top of the text box; ReportLab wants the baseline
        baseline_rl_y = self._rl_y(y_pt + ascender)
        self._canvas.drawString(draw_x, baseline_rl_y, text)

        return y_pt + size_pt  # return bottom of text box

    def measure_text_width(self, text: str, font_name: str, size_pt: float) -> float:
        from reportlab.pdfbase import pdfmetrics

        registered_name = register_rl_font(font_name)
        return pdfmetrics.stringWidth(text, registered_name, size_pt)

    def draw_image(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        image: Image.Image,
    ) -> None:
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(buf)
        rl_y = self._rl_y(y_pt, h_pt)
        self._canvas.drawImage(img_reader, self._rl_x(x_pt), rl_y, w_pt, h_pt, mask="auto")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _truncate_text_rl(
        self, text: str, font_name: str, size_pt: float, max_width_pt: float
    ) -> str:
        from reportlab.pdfbase import pdfmetrics

        ellipsis = "…"
        if pdfmetrics.stringWidth(text, font_name, size_pt) <= max_width_pt:
            return text
        while text and pdfmetrics.stringWidth(text + ellipsis, font_name, size_pt) > max_width_pt:
            text = text[:-1]
        return text + ellipsis


# ---------------------------------------------------------------------------
# Concrete: Image render context (Pillow)
# ---------------------------------------------------------------------------

class ImageRenderContext(RenderContext):
    """Pillow-backed render context for PNG/JPEG preview output.

    Coordinates are still in points (top-left origin, Y down) and are converted
    to pixels internally using the card's DPI setting.
    """

    def __init__(self, image: Image.Image, spec: "CardSpec", tokens: DesignTokens) -> None:
        super().__init__(spec, tokens)
        self._image = image
        self._draw = ImageDraw.Draw(image)
        self._dpi = spec.dpi
        self._bleed_px = spec.bleed_px

    def _to_px(self, pt: float) -> int:
        """Convert points to pixels at the card's DPI."""
        return round(pt * self._dpi / 72.0)

    def _coord_px(self, x_pt: float, y_pt: float) -> tuple[int, int]:
        """Convert card-space point coordinates to image-space pixels."""
        return (self._to_px(x_pt) + self._bleed_px, self._to_px(y_pt) + self._bleed_px)

    # ------------------------------------------------------------------
    # RenderContext interface
    # ------------------------------------------------------------------

    def fill_background(self, color: tuple[int, int, int]) -> None:
        self._draw.rectangle(
            [0, 0, self._image.width - 1, self._image.height - 1], fill=color
        )

    def draw_rect(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        fill: tuple[int, int, int],
        stroke: Optional[tuple[int, int, int]] = None,
        stroke_width_pt: float = 0.5,
    ) -> None:
        x0, y0 = self._coord_px(x_pt, y_pt)
        x1 = x0 + self._to_px(w_pt)
        y1 = y0 + self._to_px(h_pt)
        self._draw.rectangle([x0, y0, x1, y1], fill=fill)
        if stroke:
            lw = max(1, self._to_px(stroke_width_pt))
            self._draw.rectangle([x0, y0, x1, y1], outline=stroke, width=lw)

    def draw_line(
        self,
        x1_pt: float,
        y1_pt: float,
        x2_pt: float,
        y2_pt: float,
        color: tuple[int, int, int],
        width_pt: float = 0.5,
    ) -> None:
        x1, y1 = self._coord_px(x1_pt, y1_pt)
        x2, y2 = self._coord_px(x2_pt, y2_pt)
        lw = max(1, self._to_px(width_pt))
        self._draw.line([(x1, y1), (x2, y2)], fill=color, width=lw)

    def draw_text(
        self,
        x_pt: float,
        y_pt: float,
        text: str,
        font_name: str,
        size_pt: float,
        color: tuple[int, int, int],
        align: str = "left",
        max_width_pt: Optional[float] = None,
    ) -> float:
        font = get_pil_font(font_name, size_pt, self._dpi)
        x_px, y_px = self._coord_px(x_pt, y_pt)

        if max_width_pt:
            text = self._truncate_text_pil(text, font, self._to_px(max_width_pt))

        text_width_px = self._measure_width_px(text, font)
        if align == "right":
            x_px = x_px - text_width_px
        elif align == "center":
            x_px = x_px - text_width_px // 2

        self._draw.text((x_px, y_px), text, font=font, fill=color)

        # Return Y of bottom of text box in points
        bbox = font.getbbox(text)
        text_height_pt = (bbox[3] - bbox[1]) * 72.0 / self._dpi
        return y_pt + text_height_pt

    def measure_text_width(self, text: str, font_name: str, size_pt: float) -> float:
        font = get_pil_font(font_name, size_pt, self._dpi)
        width_px = self._measure_width_px(text, font)
        return width_px * 72.0 / self._dpi

    def draw_image(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        image: Image.Image,
    ) -> None:
        x_px, y_px = self._coord_px(x_pt, y_pt)
        w_px = self._to_px(w_pt)
        h_px = self._to_px(h_pt)
        resized = image.resize((w_px, h_px), Image.LANCZOS)
        if resized.mode in ("RGBA", "LA"):
            self._image.paste(resized, (x_px, y_px), resized.split()[-1])
        else:
            self._image.paste(resized, (x_px, y_px))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _measure_width_px(self, text: str, font: ImageFont.FreeTypeFont) -> int:
        try:
            return round(font.getlength(text))
        except AttributeError:
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0]

    def _truncate_text_pil(
        self, text: str, font: ImageFont.FreeTypeFont, max_px: int
    ) -> str:
        ellipsis = "…"
        if self._measure_width_px(text, font) <= max_px:
            return text
        while text and self._measure_width_px(text + ellipsis, font) > max_px:
            text = text[:-1]
        return text + ellipsis


# ---------------------------------------------------------------------------
# BaseTemplate
# ---------------------------------------------------------------------------

class BaseTemplate(ABC):
    """Abstract card template.

    To create a new card style:

    1. Subclass :class:`BaseTemplate`.
    2. Override :attr:`name`, :attr:`description`, :meth:`design_tokens`, and
       :meth:`render`.
    3. Register the subclass with :class:`~bizcard.templates.registry.TemplateRegistry`.

    The :meth:`render_back` method has a default implementation (blank card
    face) but can be overridden for a custom back-side design.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique slug used to select this template from the CLI, e.g. ``"claude-minimal"``."""

    @property
    @abstractmethod
    def description(self) -> str:
        """One-line human-readable description shown in ``bizcard list-templates``."""

    @abstractmethod
    def design_tokens(self) -> DesignTokens:
        """Return the :class:`DesignTokens` for this template."""

    @abstractmethod
    def render(self, contact: "Contact", ctx: RenderContext) -> None:
        """Draw the front face of the card onto *ctx*.

        Args:
            contact: The contact record to render.
            ctx: The drawing surface.  All methods accept point coordinates with
                 the origin at the top-left of the trim box.
        """

    def render_back(self, contact: "Contact", ctx: RenderContext) -> None:
        """Draw the back face of the card (default: blank background).

        Override to add a logo, pattern, or other back-side content.
        """
        tokens = self.design_tokens()
        ctx.fill_background(hex_to_rgb(tokens.bg_color))
