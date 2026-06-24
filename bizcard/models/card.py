"""Card specification model.

:class:`CardSpec` describes the physical card — dimensions, orientation, bleed,
and DPI — independent of any particular contact or template.  Renderers consume
this to set up their canvases correctly.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Orientation(str, Enum):
    """Card orientation."""

    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class CardSpec(BaseModel):
    """Physical specification of a business card.

    All measurements are stored in inches so they are DPI-agnostic.  Point and
    pixel equivalents are provided as computed properties.

    Attributes:
        width_in: Card width in inches (excluding bleed).
        height_in: Card height in inches (excluding bleed).
        bleed_in: Bleed extension on each side in inches.
        safe_margin_in: Safe-zone inset from the trim edge in inches.
        dpi: Dots-per-inch for raster output.
        orientation: Landscape or portrait.
    """

    width_in: float = Field(default=3.5, gt=0, description="Card width in inches (no bleed)")
    height_in: float = Field(default=2.0, gt=0, description="Card height in inches (no bleed)")
    bleed_in: float = Field(default=0.125, ge=0, description="Bleed on each edge in inches")
    safe_margin_in: float = Field(default=0.125, ge=0, description="Safe-zone margin in inches")
    dpi: int = Field(default=300, ge=72, le=1200)
    orientation: Orientation = Field(default=Orientation.LANDSCAPE)

    @model_validator(mode="after")
    def _apply_orientation(self) -> "CardSpec":
        """Swap width/height if portrait is requested and dimensions are landscape."""
        if self.orientation == Orientation.PORTRAIT and self.width_in > self.height_in:
            w, h = self.width_in, self.height_in
            object.__setattr__(self, "width_in", h)
            object.__setattr__(self, "height_in", w)
        return self

    # ------------------------------------------------------------------
    # Point equivalents (1 pt = 1/72 inch) — used by ReportLab
    # ------------------------------------------------------------------

    @property
    def width_pt(self) -> float:
        return self.width_in * 72.0

    @property
    def height_pt(self) -> float:
        return self.height_in * 72.0

    @property
    def bleed_pt(self) -> float:
        return self.bleed_in * 72.0

    @property
    def safe_margin_pt(self) -> float:
        return self.safe_margin_in * 72.0

    # Full canvas including bleed
    @property
    def canvas_width_pt(self) -> float:
        return self.width_pt + 2 * self.bleed_pt

    @property
    def canvas_height_pt(self) -> float:
        return self.height_pt + 2 * self.bleed_pt

    # ------------------------------------------------------------------
    # Pixel equivalents — used by Pillow
    # ------------------------------------------------------------------

    @property
    def width_px(self) -> int:
        return round(self.width_in * self.dpi)

    @property
    def height_px(self) -> int:
        return round(self.height_in * self.dpi)

    @property
    def bleed_px(self) -> int:
        return round(self.bleed_in * self.dpi)

    @property
    def safe_margin_px(self) -> int:
        return round(self.safe_margin_in * self.dpi)

    @property
    def canvas_width_px(self) -> int:
        return self.width_px + 2 * self.bleed_px

    @property
    def canvas_height_px(self) -> int:
        return self.height_px + 2 * self.bleed_px

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def pt_to_px(self, pt: float) -> int:
        """Convert a point measurement to pixels at this card's DPI."""
        return round(pt * self.dpi / 72.0)

    def px_to_pt(self, px: int) -> float:
        """Convert pixels to points at this card's DPI."""
        return px * 72.0 / self.dpi

    @classmethod
    def standard_landscape(cls, dpi: int = 300) -> "CardSpec":
        """Standard 3.5 × 2 inch landscape card at *dpi* resolution."""
        return cls(width_in=3.5, height_in=2.0, dpi=dpi, orientation=Orientation.LANDSCAPE)

    @classmethod
    def standard_portrait(cls, dpi: int = 300) -> "CardSpec":
        """Standard 2 × 3.5 inch portrait card at *dpi* resolution."""
        return cls(width_in=2.0, height_in=3.5, dpi=dpi, orientation=Orientation.PORTRAIT)

    def __repr__(self) -> str:
        return (
            f"CardSpec({self.width_in}×{self.height_in}in, "
            f"{self.dpi}dpi, {self.orientation.value})"
        )
