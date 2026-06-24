#!/usr/bin/env python3
"""
bizcard — Example usage as a Python library.

Demonstrates the full pipeline:
1. Load a CSV of contacts
2. Validate and normalise each record
3. Apply the claude-minimal template
4. Render and export individual PDFs
5. Export a single contact-sheet proof PDF

Run from the repository root::

    pip install -e .
    python scripts/download_fonts.py   # one-time font setup
    python examples/example_usage.py
"""

from __future__ import annotations

import logging
from pathlib import Path

# ── Configure logging before anything else ───────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── bizcard imports ───────────────────────────────────────────────────────────
from bizcard.models.card import CardSpec
from bizcard.models.contact import Contact
from bizcard.services.export import ExportService
from bizcard.services.ingest import IngestService
from bizcard.services.render import RenderService
from bizcard.templates.registry import TemplateRegistry


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("./output/examples")
CSV_PATH = Path(__file__).parent / "sample_contacts.csv"
TEMPLATE_NAME = "claude-minimal"
DPI = 300          # print-ready
PREVIEW_DPI = 150  # for PNG previews


# ---------------------------------------------------------------------------
# Step 1 — Load and validate contacts
# ---------------------------------------------------------------------------

def load_contacts(csv_path: Path) -> list[Contact]:
    log.info("Loading contacts from %s", csv_path)
    ingest = IngestService()
    contacts = ingest.from_csv(csv_path, skip_errors=True)
    log.info("Loaded %d valid contact(s)", len(contacts))
    for i, c in enumerate(contacts, 1):
        log.info("  [%2d] %-30s %s", i, c.name, c.email or "(no email)")
    return contacts


# ---------------------------------------------------------------------------
# Step 2 — Select template and configure renderer / exporter
# ---------------------------------------------------------------------------

def setup_pipeline(output_dir: Path) -> tuple[RenderService, ExportService]:
    spec = CardSpec.standard_landscape(dpi=DPI)
    renderer = RenderService(spec=spec)
    exporter = ExportService(output_dir=output_dir, renderer=renderer)
    log.info("Output directory: %s", output_dir.resolve())
    return renderer, exporter


# ---------------------------------------------------------------------------
# Step 3 — Render individual cards
# ---------------------------------------------------------------------------

def render_individual_cards(
    contacts: list[Contact],
    template_name: str,
    exporter: ExportService,
) -> None:
    log.info("Rendering %d individual cards with template '%s' …", len(contacts), template_name)
    template = TemplateRegistry.get(template_name)

    results = exporter.generate_batch(
        contacts,
        template,
        pdf=True,
        png=True,
        include_back=False,
        preview_dpi=PREVIEW_DPI,
    )

    for contact, paths in zip(contacts, results):
        for fmt, path in paths.items():
            log.info("  %-8s %s", f"[{fmt.upper()}]", path.name)


# ---------------------------------------------------------------------------
# Step 4 — Contact-sheet proof PDF
# ---------------------------------------------------------------------------

def render_contact_sheet(
    contacts: list[Contact],
    template_name: str,
    exporter: ExportService,
) -> None:
    log.info("Rendering contact-sheet proof PDF …")
    template = TemplateRegistry.get(template_name)
    path = exporter.generate_contact_sheet(
        contacts,
        template,
        output_name="contact_sheet_proof.pdf",
        cards_per_row=2,
        preview_dpi=PREVIEW_DPI,
    )
    log.info("  [SHEET] %s", path.name)


# ---------------------------------------------------------------------------
# Programmatic API example — single card
# ---------------------------------------------------------------------------

def single_card_api_example() -> None:
    """Demonstrate the programmatic API for a single contact."""
    log.info("─" * 60)
    log.info("Single-card API example")

    contact = Contact(
        name="Alexandra Voss",
        title="Chief Technology Officer",
        company="Axiom Systems",
        email="alexandra@axiom.io",
        phone="+1 415 555 8800",
        website="axiom.io",
        linkedin="in/alexandravoss",
    )

    spec = CardSpec.standard_landscape(dpi=DPI)
    renderer = RenderService(spec=spec)
    template = TemplateRegistry.get(TEMPLATE_NAME)

    # Render to in-memory bytes
    pdf_bytes = renderer.render_pdf(contact, template)
    preview_img = renderer.render_image(contact, template, dpi=PREVIEW_DPI)

    log.info("  Rendered PDF: %d bytes", len(pdf_bytes))
    log.info("  Rendered image: %dx%d px", preview_img.width, preview_img.height)

    # Export to disk
    exporter = ExportService(output_dir=OUTPUT_DIR)
    paths = exporter.generate_card(contact, template, pdf=True, png=True)
    for fmt, path in paths.items():
        log.info("  %-8s %s", f"[{fmt.upper()}]", path.name)

    # Dark variant
    dark_template = TemplateRegistry.get("claude-dark")
    dark_paths = exporter.generate_card(contact, dark_template, pdf=True, png=True)
    for fmt, path in dark_paths.items():
        log.info("  %-8s %s (dark)", f"[{fmt.upper()}]", path.name)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    log.info("=" * 60)
    log.info("bizcard — example pipeline")
    log.info("=" * 60)

    renderer, exporter = setup_pipeline(OUTPUT_DIR)

    # Batch pipeline
    contacts = load_contacts(CSV_PATH)
    render_individual_cards(contacts, TEMPLATE_NAME, exporter)
    render_contact_sheet(contacts, TEMPLATE_NAME, exporter)

    # Single-card API demo
    single_card_api_example()

    log.info("=" * 60)
    log.info("Done.  Output in: %s", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()
