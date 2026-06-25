"""PDF generation — wraps bizcard.services.render into in-memory bytes + MD5."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

# Ensure the project root is on sys.path so bizcard is importable in Vercel
sys.path.insert(0, str(Path(__file__).parent.parent))

from bizcard.models.card import CardSpec
from bizcard.models.contact import Contact
from bizcard.services.render import RenderService
from bizcard.templates.registry import TemplateRegistry


def generate_pdf_bytes(req) -> tuple[bytes, str]:
    """Generate a tpo-standard business card PDF and return (bytes, md5hex).

    Args:
        req: CardOrderRequest with name, title, email, phone, signal, linkedin.

    Returns:
        Tuple of raw PDF bytes and their lowercase MD5 hex digest.
    """
    contact = Contact(
        name=req.name,
        title=req.title or None,
        email=req.email or None,
        phone=req.phone or None,
        signal=req.signal or None,
        linkedin=req.linkedin or None,
    )

    spec = CardSpec.standard_landscape(dpi=300)
    template = TemplateRegistry.get("tpo-standard")
    renderer = RenderService(spec=spec, include_bleed=True)

    pdf_bytes = renderer.render_pdf(contact, template, include_back=True)
    md5 = hashlib.md5(pdf_bytes).hexdigest()
    return pdf_bytes, md5
