"""Contact data model with validation and normalisation.

The :class:`Contact` class is the canonical representation of a person's
business card data.  It is intentionally kept simple: plain fields with light
validation, a few computed properties, and no rendering logic.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


_PHONE_STRIP_RE = re.compile(r"[^\d+\-\s().xX]")


class Contact(BaseModel):
    """All fields that can appear on a business card.

    Only ``name`` is required.  Optional fields that are ``None`` collapse
    gracefully in the layout engine — no blank gaps are rendered.

    Attributes:
        name: Full display name, e.g. ``"Jane Smith"``.
        title: Job title, e.g. ``"Senior Engineer"``.
        company: Organisation name.
        email: Primary email address (normalised to lowercase).
        phone: Phone number in any format; stored as-provided after stripping
            unusual characters.
        website: URL without protocol prefix (displayed as-is).
        linkedin: LinkedIn profile URL or handle (``in/handle``).
        address: Mailing address (single line or multi-line).
        logo_path: Path to a logo file (PNG/SVG).  Resolved at render time.
        qr_url: URL encoded into an optional QR code on the card.
    """

    name: str = Field(..., min_length=1, max_length=120)
    title: Optional[str] = Field(default=None, max_length=120)
    company: Optional[str] = Field(default=None, max_length=120)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None, max_length=40)
    website: Optional[str] = Field(default=None, max_length=200)
    linkedin: Optional[str] = Field(default=None, max_length=200)
    address: Optional[str] = Field(default=None, max_length=200)
    logo_path: Optional[Path] = Field(default=None)
    qr_url: Optional[str] = Field(default=None, max_length=2000)

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("name", mode="before")
    @classmethod
    def _normalise_name(cls, v: object) -> str:
        if not isinstance(v, str):
            raise ValueError("name must be a string")
        return " ".join(str(v).split())  # collapse internal whitespace

    @field_validator("email", mode="before")
    @classmethod
    def _normalise_email(cls, v: object) -> Optional[str]:
        if v is None or str(v).strip() == "":
            return None
        return str(v).strip().lower()

    @field_validator("phone", mode="before")
    @classmethod
    def _normalise_phone(cls, v: object) -> Optional[str]:
        if v is None or str(v).strip() == "":
            return None
        # Remove characters that are definitely not phone-related
        cleaned = _PHONE_STRIP_RE.sub("", str(v).strip())
        return cleaned or None

    @field_validator("website", mode="before")
    @classmethod
    def _normalise_website(cls, v: object) -> Optional[str]:
        if v is None or str(v).strip() == "":
            return None
        url = str(v).strip()
        # Strip protocol for cleaner display on the card face
        url = re.sub(r"^https?://", "", url).rstrip("/")
        return url or None

    @field_validator("linkedin", mode="before")
    @classmethod
    def _normalise_linkedin(cls, v: object) -> Optional[str]:
        if v is None or str(v).strip() == "":
            return None
        raw = str(v).strip()
        # Accept full URL or bare handle and normalise to "in/<handle>"
        m = re.search(r"linkedin\.com/in/([^/?\s]+)", raw, re.IGNORECASE)
        if m:
            return f"in/{m.group(1)}"
        if raw.startswith("in/") or raw.startswith("/in/"):
            return raw.lstrip("/")
        if "/" not in raw:
            return f"in/{raw}"
        return raw

    @field_validator("logo_path", mode="before")
    @classmethod
    def _coerce_logo_path(cls, v: object) -> Optional[Path]:
        if v is None or str(v).strip() == "":
            return None
        return Path(str(v))

    @model_validator(mode="after")
    def _strip_empty_strings(self) -> "Contact":
        """Ensure blank/whitespace-only strings become None for optional text fields."""
        for field in ("title", "company", "address", "qr_url"):
            val = getattr(self, field)
            if val is not None and str(val).strip() == "":
                object.__setattr__(self, field, None)
        return self

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def first_name(self) -> str:
        """First word of the name."""
        parts = self.name.split()
        return parts[0] if parts else ""

    @property
    def last_name(self) -> str:
        """Everything after the first word of the name."""
        parts = self.name.split()
        return " ".join(parts[1:]) if len(parts) > 1 else ""

    @property
    def initials(self) -> str:
        """Up to two uppercase initials derived from the name."""
        parts = [p for p in self.name.split() if p]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def output_filename_stem(self) -> str:
        """Predictable filename stem: ``{last}_{first}`` in lowercase.

        Uses only the final word of the name as the sort-key surname so that
        "Jane Marie Smith" → "smith_jane", not "mariesmith_jane".
        """
        parts = self.name.split()
        first = re.sub(r"[^\w]", "", parts[0]).lower() if parts else ""
        last = re.sub(r"[^\w]", "", parts[-1]).lower() if len(parts) > 1 else ""
        if last and first:
            return f"{last}_{first}"
        return re.sub(r"[^\w]", "_", self.name).lower()

    @property
    def contact_fields(self) -> list[tuple[str, str]]:
        """Ordered list of ``(label, value)`` pairs for non-empty contact fields.

        Returns only fields that have a value, in display-priority order.
        """
        candidates = [
            ("company", self.company),
            ("email", self.email),
            ("phone", self.phone),
            ("web", self.website),
            ("linkedin", self.linkedin),
            ("address", self.address),
        ]
        return [(label, value) for label, value in candidates if value]

    def __str__(self) -> str:
        return f"Contact({self.name!r})"

    def __repr__(self) -> str:
        fields = {k: v for k, v in self.model_dump().items() if v is not None}
        return f"Contact({fields!r})"
