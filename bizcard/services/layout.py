"""Layout engine — resolves per-contact layout decisions before render.

The :class:`LayoutEngine` is a thin service that sits between data ingestion
and rendering.  It examines a :class:`~bizcard.models.contact.Contact` and
:class:`~bizcard.models.card.CardSpec` and produces a :class:`LayoutPlan` —
a resolved record of what fields will appear and in which positions.

Templates may consult the plan, but the current built-in templates compute
their own layout directly inside :meth:`~bizcard.templates.base.BaseTemplate.render`.
The plan is kept as a separate artefact so future templates and renderers can
consume a pre-computed layout without repeating field-visibility logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from bizcard.models.card import CardSpec
    from bizcard.models.contact import Contact

log = logging.getLogger(__name__)


@dataclass
class FieldEntry:
    """A single resolved field ready for rendering.

    Attributes:
        key: Logical field name (e.g. ``"email"``).
        value: The display string.
        y_pt: Suggested Y position from top of card in points.
        font_name: Suggested font name.
        size_pt: Suggested font size in points.
        color_token: Colour token name from the design token set
            (``"text_primary"``, ``"text_secondary"``, etc.).
    """

    key: str
    value: str
    y_pt: float = 0.0
    font_name: str = "Inter-Regular"
    size_pt: float = 8.0
    color_token: str = "text_secondary"


@dataclass
class LayoutPlan:
    """Pre-computed layout decisions for a single card face.

    Attributes:
        name_entry: Resolved name field.
        title_entry: Resolved title field (or ``None``).
        contact_entries: Ordered list of contact detail fields that fit within
            the card safe zone.
        has_logo: Whether a logo image will be rendered.
        has_monogram: Whether an initials monogram will be rendered.
        has_qr: Whether a QR code will be rendered.
        rule_y_pt: Y position of the accent rule in points.
        contact_max_width_pt: Available width for the contact text column.
    """

    name_entry: FieldEntry
    title_entry: Optional[FieldEntry] = None
    contact_entries: list[FieldEntry] = field(default_factory=list)
    has_logo: bool = False
    has_monogram: bool = False
    has_qr: bool = False
    rule_y_pt: float = 0.0
    contact_max_width_pt: float = 0.0


class LayoutEngine:
    """Resolves layout decisions for a contact + card specification pair.

    Example::

        engine = LayoutEngine()
        plan = engine.plan(contact, card_spec, template)
    """

    def plan(
        self,
        contact: "Contact",
        spec: "CardSpec",
        template_tokens: object,  # DesignTokens
    ) -> LayoutPlan:
        """Compute a :class:`LayoutPlan` for the given contact and card.

        Determines which fields fit within the safe zone, where the accent rule
        falls, and whether a logo, monogram, or QR code will be rendered.

        Args:
            contact: The contact record.
            spec: Physical card dimensions.
            template_tokens: :class:`~bizcard.config.DesignTokens` from the
                chosen template.

        Returns:
            A fully resolved :class:`LayoutPlan`.
        """
        t = template_tokens
        card_w = spec.width_pt
        card_h = spec.height_pt

        # Accent rule
        rule_y = card_h * t.accent_rule_y_ratio

        # Logo / monogram flags
        has_logo = bool(
            contact.logo_path and contact.logo_path.exists()
        )
        has_monogram = not has_logo and bool(contact.initials)
        has_qr = bool(contact.qr_url)

        # Name block
        name_entry = FieldEntry(
            key="name",
            value=contact.name,
            y_pt=t.margin_top + 2.0,
            font_name=t.font_display,
            size_pt=t.size_name,
            color_token="text_primary",
        )

        # Title
        title_entry: Optional[FieldEntry] = None
        if contact.title:
            title_y = name_entry.y_pt + t.size_name + t.line_gap
            title_entry = FieldEntry(
                key="title",
                value=contact.title,
                y_pt=title_y,
                font_name=t.font_body,
                size_pt=t.size_title,
                color_token="text_secondary",
            )

        # Contact block
        right_bound = card_w - t.margin_right
        if has_qr:
            right_bound -= t.qr_size_pt + t.qr_padding_pt
        if has_logo or has_monogram:
            # Logo zone occupies top-right; contact block has full width below rule
            pass

        contact_max_w = right_bound - t.margin_left
        y_contact = rule_y + t.section_gap
        bottom_limit = card_h - t.margin_bottom

        contact_entries: list[FieldEntry] = []
        for label, value in contact.contact_fields:
            if y_contact >= bottom_limit:
                log.debug("Truncating contact fields: card height exceeded at '%s'", label)
                break
            size = t.size_company if label == "company" else t.size_detail
            font = t.font_medium if label == "company" else t.font_body
            color = "text_primary" if label == "company" else "text_secondary"
            contact_entries.append(
                FieldEntry(
                    key=label,
                    value=value,
                    y_pt=y_contact,
                    font_name=font,
                    size_pt=size,
                    color_token=color,
                )
            )
            y_contact += size + t.line_gap

        return LayoutPlan(
            name_entry=name_entry,
            title_entry=title_entry,
            contact_entries=contact_entries,
            has_logo=has_logo,
            has_monogram=has_monogram,
            has_qr=has_qr,
            rule_y_pt=rule_y,
            contact_max_width_pt=contact_max_w,
        )
