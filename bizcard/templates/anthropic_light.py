"""AnthropicLightTemplate — authentic Anthropic brand palette.

Design tokens extracted directly from anthropic.com CSS:

  Background  #E8E6DC — warm ivory/cream (--swatch--cloud-light family)
  Text dark   #141413 — near-black with a warm, organic undertone
  Text mid    #30302E — dark warm-grey for secondary type
  Text muted  #87867F — warm grey for tertiary labels
  Terracotta  #D97757 — the actual brand accent (more orange than our prior approx.)

Compared to claude-minimal:
- The ivory background gives the card warmth rather than clinical white
- #141413 is very close to #1A1A1A but shifts slightly warm
- #D97757 is more orange-coral vs the #C96A3A copper we used before
- The overall feel is softer and more editorial

Typography note:
  Anthropic's website uses a proprietary serif for display headings.
  This template will use "Tiempos-Text" or "Libre Baskerville" if present
  in assets/fonts/, falling back to Inter-Bold, so the card reads
  correctly even without the proprietary face.
"""

from __future__ import annotations

from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import RenderContext
from bizcard.templates.claude_minimal import ClaudeMinimalTemplate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bizcard.models.contact import Contact


class AnthropicLightTemplate(ClaudeMinimalTemplate):
    """Warm ivory card using the authentic anthropic.com colour palette.

    Inherits all layout geometry from :class:`ClaudeMinimalTemplate`.
    Only the design tokens (palette) differ.
    """

    @property
    def name(self) -> str:
        return "anthropic-light"

    @property
    def description(self) -> str:
        return "Warm ivory (#E8E6DC) background, authentic Anthropic palette from anthropic.com"

    def design_tokens(self) -> DesignTokens:
        """Authentic Anthropic brand tokens extracted from anthropic.com CSS."""
        return DesignTokens(
            # ── Palette — sourced from anthropic.com CSS ──────────────
            bg_color="#E8E6DC",          # --swatch--cloud-light / warm ivory
            text_primary="#141413",      # primary near-black (warmer than pure #1A1A1A)
            text_secondary="#30302E",    # dark warm-grey secondary
            text_tertiary="#87867F",     # muted warm-grey for small labels
            accent_color="#D97757",      # authentic terracotta/coral (vs our prior #C96A3A)
            # ── Typography — TPO design system fonts ─────────────────
            # Newsreader is the editorial serif from the TPO design system.
            # It pairs well with the warm ivory palette of the Anthropic card.
            # Tiempos-Text-Bold (Anthropic proprietary) supersedes it if present.
            font_display="Tiempos-Text-Bold",   # falls back to Newsreader-SemiBold → Times-Bold
            font_body="HankenGrotesk-Regular",   # TPO body sans — replaces Inter-Regular
            font_medium="HankenGrotesk-SemiBold",
            font_light="HankenGrotesk-Light",
            # ── Font sizes (pt) — identical to claude-minimal ─────────
            size_name=18.0,
            size_title=9.0,
            size_company=8.5,
            size_detail=8.0,
            size_small=7.5,
            # ── Spacing — identical to claude-minimal ─────────────────
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
        """Ivory back face with a centred terracotta accent mark."""
        t = self.design_tokens()
        bg = hex_to_rgb(t.bg_color)
        accent = hex_to_rgb(t.accent_color)

        ctx.fill_background(bg)
        W = ctx.card_width_pt
        H = ctx.card_height_pt
        ctx.draw_line(
            W * 0.15, H / 2,
            W * 0.85, H / 2,
            color=accent,
            width_pt=t.accent_rule_width,
        )
