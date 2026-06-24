"""Global configuration and design token definitions.

All design tokens live here so the visual system can be updated in one place.
Settings are loaded from environment variables (prefix ``BIZCARD_``) or a
``.env`` file, with sensible defaults for local development.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------------------------------------------------------------------------
# Package paths
# ---------------------------------------------------------------------------

PACKAGE_ROOT = Path(__file__).parent
ASSETS_DIR = PACKAGE_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert ``#RRGGBB`` hex string to an (R, G, B) integer tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def hex_to_rgb_float(hex_color: str) -> tuple[float, float, float]:
    """Convert ``#RRGGBB`` hex string to an (R, G, B) float tuple in [0, 1]."""
    r, g, b = hex_to_rgb(hex_color)
    return r / 255.0, g / 255.0, b / 255.0


# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

class DesignTokens(BaseModel):
    """Immutable palette + typography specification for a card theme.

    All colour values are ``#RRGGBB`` hex strings.  Point sizes follow standard
    print conventions (1 pt = 1/72 inch).
    """

    # --- Palette ---
    bg_color: str = "#FFFFFF"
    text_primary: str = "#1A1A1A"
    text_secondary: str = "#6B6B6B"
    text_tertiary: str = "#9A9A94"
    accent_color: str = "#C96A3A"

    # --- Typography ---
    font_display: str = "Inter-Bold"
    font_body: str = "Inter-Regular"
    font_medium: str = "Inter-Medium"
    font_light: str = "Inter-Light"

    # Font sizes in points
    size_name: float = 18.0
    size_title: float = 9.0
    size_company: float = 8.5
    size_detail: float = 8.0
    size_small: float = 7.5

    # --- Spacing (points) ---
    margin_left: float = 14.0
    margin_right: float = 14.0
    margin_top: float = 12.0
    margin_bottom: float = 12.0
    line_gap: float = 4.0        # gap between adjacent text lines
    section_gap: float = 10.0    # gap between major layout sections

    # --- Accent rule ---
    accent_rule_width: float = 0.5   # line weight in points
    accent_rule_y_ratio: float = 0.48  # vertical position as fraction of card height

    # --- Logo zone ---
    logo_size_pt: float = 28.0       # max dimension for logo/monogram area
    logo_padding_pt: float = 4.0     # padding around the logo

    # --- QR code ---
    qr_size_pt: float = 48.0        # QR code box size in points
    qr_padding_pt: float = 4.0


# ---------------------------------------------------------------------------
# Application settings
# ---------------------------------------------------------------------------

class BizCardSettings(BaseSettings):
    """Runtime settings loaded from environment or ``.env`` file.

    Override any value by setting ``BIZCARD_<UPPER_NAME>`` in the environment::

        BIZCARD_OUTPUT_DIR=/tmp/cards
        BIZCARD_DPI=600
    """

    model_config = SettingsConfigDict(
        env_prefix="BIZCARD_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    output_dir: Path = Field(default=Path("./output"), description="Default output directory")
    dpi: int = Field(default=300, ge=72, le=1200, description="Print DPI")
    preview_dpi: int = Field(default=150, ge=72, le=600, description="Screen-preview DPI")
    default_template: str = Field(default="claude-minimal", description="Template name")
    default_orientation: Literal["landscape", "portrait"] = Field(default="landscape")
    include_bleed: bool = Field(default=True, description="Add bleed area to PDF output")
    bleed_in: float = Field(default=0.125, description="Bleed in inches")
    safe_margin_in: float = Field(default=0.125, description="Safe-zone inset in inches")

    @field_validator("output_dir", mode="before")
    @classmethod
    def _coerce_path(cls, v: object) -> Path:
        return Path(str(v))


# Singleton settings instance — import this elsewhere
settings = BizCardSettings()
