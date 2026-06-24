"""AnthropicDarkTemplate — near-black variant of the authentic Anthropic palette.

Uses the actual dark colour `#141413` from anthropic.com as the background
and flips text to the ivory `#E8E6DC`.  The terracotta accent `#D97757`
is identical in both variants — consistent with how Anthropic applies it.

This matches the dark/inverted treatment seen on anthropic.com's dark-mode
and hero sections.
"""

from __future__ import annotations

from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import RenderContext
from bizcard.templates.claude_minimal import ClaudeMinimalTemplate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bizcard.models.contact import Contact


class AnthropicDarkTemplate(ClaudeMinimalTemplate):
    """Near-black card using the authentic anthropic.com colour palette.

    The background is `#141413` (the actual Anthropic near-black, not pure
    black) and the primary text is `#E8E6DC` (the brand ivory).
    """

    @property
    def name(self) -> str:
        return "anthropic-dark"

    @property
    def description(self) -> str:
        return "Near-black (#141413) background, ivory text, authentic Anthropic palette"

    def design_tokens(self) -> DesignTokens:
        """Dark-mode Anthropic tokens: near-black + ivory, same terracotta accent."""
        return DesignTokens(
            # ── Palette — dark inversion of anthropic.com colours ─────
            bg_color="#141413",          # authentic Anthropic near-black
            text_primary="#E8E6DC",      # brand ivory for primary text on dark
            text_secondary="#87867F",    # warm grey secondary — readable on dark
            text_tertiary="#5E5D59",     # dark taupe for smallest labels
            accent_color="#D97757",      # same terracotta — consistent across variants
            # ── Typography — TPO design system fonts ─────────────────
            font_display="Tiempos-Text-Bold",    # Tiempos if licensed; else Times-Bold
            font_body="HankenGrotesk-Regular",    # TPO body sans
            font_medium="HankenGrotesk-SemiBold",
            font_light="HankenGrotesk-Light",
            # ── Font sizes ────────────────────────────────────────────
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
        """Near-black back face with centred terracotta accent mark."""
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
