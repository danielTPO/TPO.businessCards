"""ClaudeDarkTemplate — near-black background variant.

Inherits the full layout logic from :class:`ClaudeMinimalTemplate` and
overrides only the :meth:`design_tokens` palette so that the structural
design decisions (rule position, spacing, logo zone) stay in sync between
the light and dark variants automatically.

Palette choices:
    - Background ``#0D0D0D`` — a warm near-black (not pure black) so that
      printed ink doesn't look flat.
    - Primary text ``#F5F5F0`` — off-white with a warm tint to avoid harsh
      contrast and reduce halation on coated stock.
    - Secondary text ``#9A9A94`` — the same copper-grey used on the light
      card, readable against the dark background.
    - Accent ``#C96A3A`` — identical copper; the brand colour appears
      identical on both variants for cohesion in a paired set.
"""

from __future__ import annotations

from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import RenderContext
from bizcard.templates.claude_minimal import ClaudeMinimalTemplate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bizcard.models.contact import Contact


class ClaudeDarkTemplate(ClaudeMinimalTemplate):
    """Near-black background Claude design language card template.

    Inherits all layout geometry from :class:`ClaudeMinimalTemplate` — only
    the colour palette differs.  This is intentional: the two templates form
    a cohesive matched pair.
    """

    @property
    def name(self) -> str:
        return "claude-dark"

    @property
    def description(self) -> str:
        return "Near-black background (#0D0D0D), off-white text, copper accent — dark variant"

    def design_tokens(self) -> DesignTokens:
        """Dark-theme palette: same structure as light, flipped colours."""
        return DesignTokens(
            # ── Palette (dark) ────────────────────────────────────────
            bg_color="#0D0D0D",          # warm near-black card face
            text_primary="#F5F5F0",      # warm off-white — easier on coated stock
            text_secondary="#9A9A94",    # copper-grey secondary text
            text_tertiary="#6B6B6B",     # muted grey for smallest text
            accent_color="#C96A3A",      # same copper — brand identity is consistent
            # ── Typography — identical to light variant ───────────────
            font_display="Inter-Bold",
            font_body="Inter-Regular",
            font_medium="Inter-Medium",
            font_light="Inter-Light",
            # ── Font sizes (pt) — identical to light variant ──────────
            size_name=18.0,
            size_title=9.0,
            size_company=8.5,
            size_detail=8.0,
            size_small=7.5,
            # ── Spacing — identical to light variant ──────────────────
            margin_left=14.0,
            margin_right=14.0,
            margin_top=12.0,
            margin_bottom=12.0,
            line_gap=4.0,
            section_gap=10.0,
            # ── Accent rule — same position, same weight ──────────────
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
        """Dark back face with centred copper accent mark."""
        t = self.design_tokens()
        bg = hex_to_rgb(t.bg_color)
        accent = hex_to_rgb(t.accent_color)

        ctx.fill_background(bg)

        W = ctx.card_width_pt
        H = ctx.card_height_pt
        # A slightly longer accent mark on the back to fill more of the space
        ctx.draw_line(
            W * 0.15, H / 2,
            W * 0.85, H / 2,
            color=accent,
            width_pt=t.accent_rule_width,
        )
