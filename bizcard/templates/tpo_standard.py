"""TPOStandardTemplate — TPO Group two-column business card.

Visual anatomy (landscape card, 252 × 144 pt):

  ┌──────────────────────────────────────────────────────────────┐
  │                       │  Daniel Landry          [QR code]   │
  │   TPO.group           │  Intern                             │
  │   ▐▌▐▌▐▌▐▌▐▌▐▌▐▌▐▌▐▌  │                                     │
  │   (bars motif)        │  (xxx) xxx-xxxx         [QR code]   │
  │                       │  xxx@xxx.xxx            [QR code]   │
  │                       │  Signal: xxx                        │
  │                       │                                     │
  ├───────────────────────────────────────────────────────────────┤ ← emerald rule
  └──────────────────────────────────────────────────────────────┘

  Back face: emerald (#0E8E54) background, white TPO.group wordmark
  centred, "TECHNOLOGY. POLICY. OPERATIONS." tagline below.

Design tokens:
  bg_color        → #FFFFFF
  text_primary    → #0B0F0D  (--tpo-ink-900)
  text_secondary  → #243029  (--tpo-ink-700)
  accent_color    → #0E8E54  (--tpo-emerald-600)
  font_display    → HankenGrotesk-Bold
  font_body       → HankenGrotesk-Regular
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from PIL import Image

from bizcard.config import ASSETS_DIR, DesignTokens, hex_to_rgb
from bizcard.templates.base import BaseTemplate, RenderContext

if TYPE_CHECKING:
    from bizcard.models.contact import Contact

# Logo assets bundled with the package
_LOGO_BARS = ASSETS_DIR / "tpo-logo-bars.png"
_LOGO_WORDMARK = ASSETS_DIR / "tpo-logo.png"
_LOGO_WHITE = ASSETS_DIR / "tpo-logo-white.png"

# Fraction of logo-bars height to crop (removes the faint tagline at the bottom)
_BARS_CROP_RATIO = 0.72


def _load_bars_logo() -> Optional[Image.Image]:
    """Load tpo-logo-bars.png cropped to wordmark + bars (no tagline)."""
    if not _LOGO_BARS.exists():
        return None
    img = Image.open(_LOGO_BARS).convert("RGBA")
    crop_h = int(img.height * _BARS_CROP_RATIO)
    return img.crop((0, 0, img.width, crop_h))


def _load_white_wordmark() -> Optional[Image.Image]:
    """Load the white-on-transparent TPO.group wordmark."""
    if not _LOGO_WHITE.exists():
        return None
    return Image.open(_LOGO_WHITE).convert("RGBA")


class TPOStandardTemplate(BaseTemplate):
    """TPO Group standard two-column business card.

    Front: white card, logo-bars motif (left), emerald vertical divider,
           name / title / contact info / QR code (right), bottom emerald rule.
    Back:  emerald background, white wordmark centred, tagline below.
    """

    @property
    def name(self) -> str:
        return "tpo-standard"

    @property
    def description(self) -> str:
        return "TPO Group two-column card — bars logo left, contact info right, emerald accents"

    def design_tokens(self) -> DesignTokens:
        return DesignTokens(
            # ── Palette ───────────────────────────────────────────────
            bg_color="#FFFFFF",
            text_primary="#0B0F0D",       # --tpo-ink-900
            text_secondary="#243029",     # --tpo-ink-700
            text_tertiary="#586860",      # --tpo-ink-500
            accent_color="#0E8E54",       # --tpo-emerald-600
            # ── Typography ────────────────────────────────────────────
            font_display="HankenGrotesk-Bold",
            font_body="HankenGrotesk-Regular",
            font_medium="HankenGrotesk-SemiBold",
            font_light="HankenGrotesk-Light",
            # ── Font sizes (pt) ───────────────────────────────────────
            size_name=13.0,
            size_title=8.0,
            size_company=8.0,
            size_detail=7.5,
            size_small=6.5,
            # ── Spacing ───────────────────────────────────────────────
            margin_left=10.0,
            margin_right=10.0,
            margin_top=11.0,
            margin_bottom=11.0,
            line_gap=3.0,
            section_gap=8.0,
            # ── Accent rule (unused ratio field — rule is always at bottom) ──
            accent_rule_width=0.5,
            accent_rule_y_ratio=0.97,
            # ── Logo / QR ─────────────────────────────────────────────
            logo_size_pt=28.0,
            logo_padding_pt=4.0,
            qr_size_pt=30.0,
            qr_padding_pt=3.0,
        )

    # ------------------------------------------------------------------
    # Front face
    # ------------------------------------------------------------------

    def render(self, contact: "Contact", ctx: RenderContext) -> None:
        t = self.design_tokens()
        bg      = hex_to_rgb(t.bg_color)
        primary = hex_to_rgb(t.text_primary)
        secondary = hex_to_rgb(t.text_secondary)
        accent  = hex_to_rgb(t.accent_color)

        W = ctx.card_width_pt
        H = ctx.card_height_pt

        # ── Background ────────────────────────────────────────────────
        ctx.fill_background(bg)

        # ── Layout constants ──────────────────────────────────────────
        DIVIDER_X  = round(W * 0.41, 1)   # ~103 pt — column split
        INNER_PAD  = 8.0                   # horizontal gap on each side of divider
        MT         = t.margin_top          # top margin
        MB         = t.margin_bottom       # bottom margin
        MR         = t.margin_right        # right margin

        col_x     = DIVIDER_X + INNER_PAD   # left edge of text column
        col_right = W - MR                  # right edge of text column

        # ── Left column: bars logo ─────────────────────────────────────
        bars = _load_bars_logo()
        if bars:
            # Fit logo inside left column with comfortable margins
            avail_w = DIVIDER_X - t.margin_left - 4.0
            avail_h = H - MT - MB - 4.0
            aspect  = bars.width / bars.height

            logo_w = avail_w
            logo_h = logo_w / aspect
            if logo_h > avail_h:
                logo_h = avail_h
                logo_w = logo_h * aspect

            # Centre horizontally within left column, centre vertically on card
            logo_x = (DIVIDER_X - logo_w) / 2
            logo_y = (H - logo_h) / 2
            ctx.draw_image(logo_x, logo_y, logo_w, logo_h, bars)

        # ── Vertical emerald divider ──────────────────────────────────
        ctx.draw_line(
            DIVIDER_X, MT,
            DIVIDER_X, H - MB,
            color=accent,
            width_pt=t.accent_rule_width,
        )

        # ── QR code (optional) ────────────────────────────────────────
        # Resolve QR URL: explicit field first, then auto-expand LinkedIn handle
        qr_url: Optional[str] = contact.qr_url
        if not qr_url and contact.linkedin:
            lk = contact.linkedin
            if lk.startswith("in/"):
                qr_url = f"https://www.linkedin.com/{lk}"
            elif not lk.startswith("http"):
                qr_url = f"https://www.linkedin.com/in/{lk}"
            else:
                qr_url = lk

        qr_image: Optional[Image.Image] = None
        if qr_url:
            from bizcard.services.qr import QRService
            qr_size_px = (
                ctx._spec.pt_to_px(t.qr_size_pt)
                if hasattr(ctx, "_spec") else 90
            )
            qr_image = QRService.generate(
                qr_url,
                size_px=qr_size_px,
                bg=bg,
                fg=primary,
            )

        qr_size = t.qr_size_pt
        qr_x    = col_right - qr_size     # right-anchored in text column

        # ── Name + Title (top of right column, full width) ────────────
        # QR code is positioned next to the contact block (lower portion),
        # so name and title span the full right column width.
        full_w = col_right - col_x

        y_cursor = MT
        y_cursor = ctx.draw_text(
            col_x, y_cursor,
            contact.name,
            font_name=t.font_display,
            size_pt=t.size_name,
            color=primary,
            max_width_pt=full_w,
        )
        y_cursor += t.line_gap

        if contact.title:
            ctx.draw_text(
                col_x, y_cursor,
                contact.title,
                font_name=t.font_body,
                size_pt=t.size_title,
                color=secondary,
                max_width_pt=full_w,
            )

        # ── Contact block (lower portion) ─────────────────────────────
        # Phone / email / signal stack on the left; QR code floats right.
        contact_y    = H * 0.495    # ≈ 71 pt — start of lower block
        contact_max_w = (qr_x - t.qr_padding_pt - col_x) if qr_image else full_w

        if contact.phone:
            contact_y = ctx.draw_text(
                col_x, contact_y,
                contact.phone,
                font_name=t.font_body,
                size_pt=t.size_detail,
                color=secondary,
                max_width_pt=contact_max_w,
            )
            contact_y += t.line_gap

        if contact.email:
            contact_y = ctx.draw_text(
                col_x, contact_y,
                contact.email,
                font_name=t.font_body,
                size_pt=t.size_detail,
                color=secondary,
                max_width_pt=contact_max_w,
            )
            contact_y += t.line_gap

        if contact.signal:
            ctx.draw_text(
                col_x, contact_y,
                f"Signal: {contact.signal}",
                font_name=t.font_body,
                size_pt=t.size_detail,
                color=secondary,
                max_width_pt=contact_max_w,
            )

        # ── QR code (right of contact block) ──────────────────────────
        if qr_image:
            ctx.draw_image(qr_x, H * 0.495, qr_size, qr_size, qr_image)

        # ── Bottom emerald rule ────────────────────────────────────────
        rule_y = H - MB * 0.55
        ctx.draw_line(0.0, rule_y, W, rule_y, color=accent, width_pt=t.accent_rule_width)

    # ------------------------------------------------------------------
    # Back face
    # ------------------------------------------------------------------

    def render_back(self, contact: "Contact", ctx: RenderContext) -> None:
        """Emerald-green back: white TPO.group wordmark centred, tagline below."""
        t = self.design_tokens()
        W = ctx.card_width_pt
        H = ctx.card_height_pt

        # Emerald-600 background — bright brand green
        ctx.fill_background(hex_to_rgb("#0E8E54"))

        white = (255, 255, 255)
        muted_white = (200, 230, 215)   # very slightly tinted for tagline

        # ── White wordmark ────────────────────────────────────────────
        wm = _load_white_wordmark()

        if wm:
            # Scale to 50 % of card width, maintain aspect ratio
            wm_w = W * 0.50
            wm_h = wm_w * (wm.height / wm.width)

            # Content block = wordmark + 8pt gap + tagline (~8pt)
            block_h = wm_h + 8.0 + 8.0
            wm_y = (H - block_h) / 2          # vertically centre the block
            wm_x = (W - wm_w) / 2

            ctx.draw_image(wm_x, wm_y, wm_w, wm_h, wm)
            tagline_y = wm_y + wm_h + 8.0
        else:
            # Fallback: render "TPO.group" as text if image is unavailable
            name_w = ctx.measure_text_width("TPO.group", t.font_display, 20.0)
            block_h = 20.0 + 8.0 + 8.0
            ty = (H - block_h) / 2
            ctx.draw_text(
                W / 2, ty,
                "TPO.group",
                font_name=t.font_display,
                size_pt=20.0,
                color=white,
                align="center",
            )
            tagline_y = ty + 22.0 + 8.0

        # ── Tagline ───────────────────────────────────────────────────
        ctx.draw_text(
            W / 2, tagline_y,
            "TECHNOLOGY. POLICY. OPERATIONS.",
            font_name=t.font_light,
            size_pt=t.size_small,
            color=muted_white,
            align="center",
        )
