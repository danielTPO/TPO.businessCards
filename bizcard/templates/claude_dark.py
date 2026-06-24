"""ClaudeDarkTemplate — TPO Group dark card (deep forest background).

Inherits all layout geometry from :class:`ClaudeMinimalTemplate` and
overrides only :meth:`design_tokens` with the TPO Group dark-mode palette
sourced from ``_ds/tpo-group-design-system/colors_and_type.css``.

TPO design token mapping:
  bg_color        → --bg-dark / --tpo-forest-900   #042B1B
  text_primary    → --fg-on-dark                   #F4F7F5
  text_secondary  → --fg-on-dark-2                 #B7C5BD
  text_tertiary   → --tpo-ink-400                  #82918A
  accent_color    → --tpo-emerald-400               #3CBE85  (lighter for visibility on dark)
  font_display    → --font-display "Newsreader" SemiBold
  font_body       → --font-sans   "Hanken Grotesk" Regular/SemiBold

The deep forest background (#042B1B) is the ``--bg-dark`` hero/footer colour
in the TPO system — the darkest point of the brand, authoritative and serious.
The emerald-400 accent (#3CBE85) is used here instead of emerald-600 to
maintain legibility against the dark ground.
"""

from __future__ import annotations

from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import RenderContext
from bizcard.templates.claude_minimal import ClaudeMinimalTemplate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bizcard.models.contact import Contact


class ClaudeDarkTemplate(ClaudeMinimalTemplate):
    """TPO Group dark card — deep forest green background, TPO design system.

    Forms a cohesive matched pair with :class:`ClaudeMinimalTemplate`.
    Only the colour palette differs; all layout geometry is inherited.
    """

    @property
    def name(self) -> str:
        return "claude-dark"

    @property
    def description(self) -> str:
        return "Deep forest (#042B1B) background, TPO Group dark palette, Newsreader + Hanken Grotesk"

    def design_tokens(self) -> DesignTokens:
        """TPO Group dark-card palette from colors_and_type.css."""
        return DesignTokens(
            # ── Palette — TPO dark mode ───────────────────────────────
            bg_color="#042B1B",          # --bg-dark / --tpo-forest-900 — deepest brand green
            text_primary="#F4F7F5",      # --fg-on-dark — warm near-white on dark
            text_secondary="#B7C5BD",    # --fg-on-dark-2 — muted green-grey secondary
            text_tertiary="#82918A",     # --tpo-ink-400 — quieter labels
            accent_color="#3CBE85",      # --tpo-emerald-400 — lighter emerald for dark bg legibility
            # ── Typography — TPO design system ────────────────────────
            font_display="Newsreader-SemiBold",
            font_body="HankenGrotesk-Regular",
            font_medium="HankenGrotesk-SemiBold",
            font_light="HankenGrotesk-Light",
            # ── Font sizes (pt) ───────────────────────────────────────
            size_name=18.0,
            size_title=9.0,
            size_company=8.5,
            size_detail=8.0,
            size_small=7.5,
            # ── Spacing ───────────────────────────────────────────────
            margin_left=14.0,
            margin_right=14.0,
            margin_top=12.0,
            margin_bottom=12.0,
            line_gap=4.0,
            section_gap=10.0,
            # ── Accent rule ───────────────────────────────────────────
            accent_rule_width=0.5,
            accent_rule_y_ratio=0.46,
            # ── Logo / monogram ───────────────────────────────────────
            logo_size_pt=28.0,
            logo_padding_pt=4.0,
            # ── QR code ───────────────────────────────────────────────
            qr_size_pt=50.0,
            qr_padding_pt=4.0,
        )

    def render_back(self, contact: "Contact", ctx: RenderContext) -> None:
        """Deep-forest back face with centred emerald accent mark."""
        t = self.design_tokens()
        ctx.fill_background(hex_to_rgb(t.bg_color))
        W = ctx.card_width_pt
        H = ctx.card_height_pt
        ctx.draw_line(
            W * 0.15, H / 2,
            W * 0.85, H / 2,
            color=hex_to_rgb(t.accent_color),
            width_pt=t.accent_rule_width,
        )
