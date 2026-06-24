"""ClaudeMinimalTemplate — TPO Group light card (white background).

Design rationale
----------------
This is the primary light-background template using the TPO Group design system
tokens sourced from ``_ds/tpo-group-design-system/colors_and_type.css``.

Visual anatomy (landscape card, 252 × 144 pt):

  ┌──────────────────────────────────────────────────────────┐
  │  [margin_top]                             [logo zone]   │
  │  Jane Smith                                  ██         │  ← name / Newsreader-SemiBold / size_name
  │  Senior Engineer                                        │  ← title / HankenGrotesk-Regular / size_title
  │                                                         │
  │ ─────────────────────────────────────────────────────── │  ← accent rule / --tpo-emerald-600 / 0.5pt
  │                                                         │
  │  Acme Corp                          ┌──────────────┐   │  ← company / HankenGrotesk-SemiBold / size_company
  │  jane@acme.com                      │              │   │  ← details / HankenGrotesk-Regular / size_detail
  │  +1 555 000 1234                    │   QR code    │   │
  │  acme.com                           │              │   │
  │                                     └──────────────┘   │
  └──────────────────────────────────────────────────────────┘

TPO design token mapping:
  bg_color        → --bg-1 / --tpo-paper    #FFFFFF
  text_primary    → --fg-1 / --tpo-ink-900  #0B0F0D
  text_secondary  → --fg-2 / --tpo-ink-700  #243029
  text_tertiary   → --fg-3 / --tpo-ink-500  #586860
  accent_color    → --fg-accent-bright / --tpo-emerald-600  #0E8E54
  font_display    → --font-display  "Newsreader" (SemiBold weight)
  font_body       → --font-sans     "Hanken Grotesk" (Regular/Medium)

The emerald rule replaces the former copper rule; it anchors the card to the
TPO brand spectrum (forest-green → emerald → teal → blue "bars" motif).
- If a QR code URL is provided it floats to the right of the contact block
- If a logo file is provided it appears top-right; otherwise initials render
  in a minimal typographic treatment using the accent colour
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PIL import Image

from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import BaseTemplate, RenderContext

if TYPE_CHECKING:
    from bizcard.models.contact import Contact


class ClaudeMinimalTemplate(BaseTemplate):
    """Light-background Claude design language card template.

    Uses ``#FFFFFF`` background with copper accent.  This is the canonical
    reference implementation — read this class before building any new template.
    """

    # ------------------------------------------------------------------
    # BaseTemplate identity
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return "claude-minimal"

    @property
    def description(self) -> str:
        return "White background, copper accent line, Inter typeface — Anthropic design language"

    def design_tokens(self) -> DesignTokens:
        """TPO Group light-card palette from colors_and_type.css."""
        return DesignTokens(
            # ── Palette — from TPO Group design system ────────────────
            bg_color="#FFFFFF",          # --bg-1 / --tpo-paper
            text_primary="#0B0F0D",      # --fg-1 / --tpo-ink-900
            text_secondary="#243029",    # --fg-2 / --tpo-ink-700
            text_tertiary="#586860",     # --fg-3 / --tpo-ink-500
            accent_color="#0E8E54",      # --fg-accent-bright / --tpo-emerald-600
            # ── Typography — TPO design system font stack ─────────────
            font_display="Newsreader-SemiBold",     # --font-display, editorial serif for the name
            font_body="HankenGrotesk-Regular",       # --font-sans, humanist grotesque for details
            font_medium="HankenGrotesk-SemiBold",    # weight for company name
            font_light="HankenGrotesk-Light",        # lighter labels
            # ── Font sizes (pt) ───────────────────────────────────────
            size_name=18.0,
            size_title=9.0,
            size_company=8.5,
            size_detail=8.0,
            size_small=7.5,
            # ── Spacing (pt) ─────────────────────────────────────────
            margin_left=14.0,
            margin_right=14.0,
            margin_top=12.0,
            margin_bottom=12.0,
            line_gap=4.0,
            section_gap=10.0,
            # ── Accent rule — TPO emerald replaces former copper ──────
            accent_rule_width=0.5,
            accent_rule_y_ratio=0.46,
            # ── Logo / monogram ───────────────────────────────────────
            logo_size_pt=28.0,
            logo_padding_pt=4.0,
            # ── QR code ───────────────────────────────────────────────
            qr_size_pt=50.0,
            qr_padding_pt=4.0,
        )

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, contact: "Contact", ctx: RenderContext) -> None:
        """Draw the front face of a Claude-minimal light card."""
        t = self.design_tokens()
        bg = hex_to_rgb(t.bg_color)
        primary = hex_to_rgb(t.text_primary)
        secondary = hex_to_rgb(t.text_secondary)
        accent = hex_to_rgb(t.accent_color)

        W = ctx.card_width_pt
        H = ctx.card_height_pt

        # ── 1. Background fill ────────────────────────────────────────
        # Flood-fill the entire canvas (includes bleed area).
        ctx.fill_background(bg)

        # ── 2. Logo zone (top-right) ──────────────────────────────────
        # Reserve the top-right corner for a logo or initials monogram.
        # The zone is a square of side logo_size_pt anchored to the top-right.
        logo_size = t.logo_size_pt
        logo_x = W - t.margin_right - logo_size
        logo_y = t.margin_top
        self._draw_logo_zone(contact, ctx, logo_x, logo_y, logo_size, t, accent, bg)

        # ── 3. Name block ─────────────────────────────────────────────
        # The name and title occupy the area to the left of the logo zone.
        name_max_w = logo_x - t.margin_left - 6.0  # 6pt gap before logo
        x_left = t.margin_left
        y_cursor = t.margin_top + 2.0  # slight top padding within the margin

        # Name — the most prominent typographic element on the card
        y_cursor = ctx.draw_text(
            x_left, y_cursor,
            contact.name,
            font_name=t.font_display,   # Inter-Bold
            size_pt=t.size_name,        # 18pt
            color=primary,              # #1A1A1A
            max_width_pt=name_max_w,
        )
        y_cursor += t.line_gap

        # Title — secondary, in the mid-grey secondary colour
        if contact.title:
            y_cursor = ctx.draw_text(
                x_left, y_cursor,
                contact.title,
                font_name=t.font_body,      # Inter-Regular
                size_pt=t.size_title,       # 9pt
                color=secondary,            # #6B6B6B
                max_width_pt=name_max_w,
            )
            y_cursor += t.line_gap * 0.5

        # ── 4. Accent rule ────────────────────────────────────────────
        # A single 0.5 pt copper line across the full card width.
        # This is the ONE decorative element in the template.
        # It runs edge-to-edge (x=0 to x=W) for full-bleed visual weight.
        rule_y = H * t.accent_rule_y_ratio
        ctx.draw_line(0.0, rule_y, W, rule_y, color=accent, width_pt=t.accent_rule_width)

        # ── 5. Contact block ──────────────────────────────────────────
        # All contact fields in a single left-anchored column below the rule.
        # If a QR code is requested, reserve the right portion for it.
        qr_image: Optional[Image.Image] = None
        if contact.qr_url:
            from bizcard.services.qr import QRService
            qr_size_px = ctx._spec.pt_to_px(t.qr_size_pt) if hasattr(ctx, "_spec") else 150
            qr_image = QRService.generate(contact.qr_url, size_px=qr_size_px, bg=bg, fg=hex_to_rgb(t.text_primary))

        contact_right_bound = W - t.margin_right
        if qr_image:
            # Reserve right column for QR
            contact_right_bound = W - t.margin_right - t.qr_size_pt - t.qr_padding_pt

        contact_max_w = contact_right_bound - x_left

        # Start contact lines just below the rule
        y_contact = rule_y + t.section_gap

        for label, value in contact.contact_fields:
            if label == "company":
                # Company gets medium weight and slightly more prominence
                y_contact = ctx.draw_text(
                    x_left, y_contact,
                    value,
                    font_name=t.font_medium,    # Inter-Medium
                    size_pt=t.size_company,     # 8.5pt
                    color=primary,
                    max_width_pt=contact_max_w,
                )
            else:
                y_contact = ctx.draw_text(
                    x_left, y_contact,
                    value,
                    font_name=t.font_body,      # Inter-Regular
                    size_pt=t.size_detail,      # 8pt
                    color=secondary,            # #6B6B6B
                    max_width_pt=contact_max_w,
                )
            y_contact += t.line_gap

            # Stop if we've reached the bottom safe zone
            if y_contact > H - t.margin_bottom:
                break

        # ── 6. QR code (optional) ─────────────────────────────────────
        if qr_image:
            qr_y = rule_y + t.section_gap
            qr_x = W - t.margin_right - t.qr_size_pt
            ctx.draw_image(qr_x, qr_y, t.qr_size_pt, t.qr_size_pt, qr_image)

    # ------------------------------------------------------------------
    # Logo / monogram helper
    # ------------------------------------------------------------------

    def _draw_logo_zone(
        self,
        contact: "Contact",
        ctx: RenderContext,
        x: float,
        y: float,
        size: float,
        t: DesignTokens,
        accent: tuple[int, int, int],
        bg: tuple[int, int, int],
    ) -> None:
        """Draw a logo image or typographic initials monogram.

        Args:
            x, y: Top-left corner of the logo zone in points.
            size: Side length of the square logo zone in points.
        """
        if contact.logo_path and contact.logo_path.exists():
            try:
                logo = Image.open(contact.logo_path).convert("RGBA")
                ctx.draw_image(x, y, size, size, logo)
                return
            except OSError:
                pass  # fall through to monogram

        # Typographic initials — rendered in the accent colour
        initials = contact.initials
        if not initials:
            return

        # Scale font size so initials fill about 70 % of the zone
        # Two initials → smaller, one initial → larger
        mono_size = size * 0.55 if len(initials) == 2 else size * 0.65
        mono_x = x + size / 2       # horizontal centre of zone
        mono_y = y + (size - mono_size) / 2   # vertically centre approx

        ctx.draw_text(
            mono_x, mono_y,
            initials,
            font_name=t.font_display,
            size_pt=mono_size,
            color=accent,            # copper initials — the sole accent element
            align="center",
        )

    # ------------------------------------------------------------------
    # Back face
    # ------------------------------------------------------------------

    def render_back(self, contact: "Contact", ctx: RenderContext) -> None:
        """Blank white back face — optionally add a centred copper accent line."""
        t = self.design_tokens()
        bg = hex_to_rgb(t.bg_color)
        accent = hex_to_rgb(t.accent_color)

        ctx.fill_background(bg)

        # A single accent line — same rhythm as the front face
        W = ctx.card_width_pt
        H = ctx.card_height_pt
        ctx.draw_line(
            W * 0.15, H / 2,
            W * 0.85, H / 2,
            color=accent,
            width_pt=t.accent_rule_width,
        )
