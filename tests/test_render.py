"""Unit tests for RenderService and ExportService.

These tests verify that:
- Rendered PDF/PNG output is non-empty
- The correct file names are generated
- Both light and dark templates render without error
- Batch rendering produces one artefact per contact
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from bizcard.models.card import CardSpec
from bizcard.models.contact import Contact
from bizcard.services.export import ExportService
from bizcard.services.render import RenderService
from bizcard.templates.registry import TemplateRegistry


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_contact():
    return Contact(
        name="Jane Smith",
        title="Senior Engineer",
        company="Acme Corp",
        email="jane@acme.com",
        phone="+1 555 000 1234",
        website="acme.com",
    )


@pytest.fixture
def full_contact():
    return Contact(
        name="Marcus Chen",
        title="Product Designer",
        company="Veridian Studio",
        email="marcus@veridian.io",
        phone="+1 415 555 9876",
        website="veridian.io",
        linkedin="in/marcuschen",
        address="San Francisco CA",
    )


@pytest.fixture
def low_dpi_spec():
    """Use 72 DPI for tests to keep them fast."""
    return CardSpec.standard_landscape(dpi=72)


@pytest.fixture
def renderer(low_dpi_spec):
    return RenderService(spec=low_dpi_spec)


@pytest.fixture
def exporter(tmp_path, renderer):
    return ExportService(output_dir=tmp_path, renderer=renderer)


# ---------------------------------------------------------------------------
# RenderService — PDF
# ---------------------------------------------------------------------------

class TestRenderPDF:
    def test_pdf_is_non_empty(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        pdf = renderer.render_pdf(simple_contact, tmpl)
        assert isinstance(pdf, bytes)
        assert len(pdf) > 1024  # a real PDF is always > 1 KB

    def test_pdf_starts_with_pdf_header(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        pdf = renderer.render_pdf(simple_contact, tmpl)
        assert pdf[:4] == b"%PDF"

    def test_pdf_with_back(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        pdf = renderer.render_pdf(simple_contact, tmpl, include_back=True)
        assert len(pdf) > 1024

    def test_dark_template_pdf(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-dark")
        pdf = renderer.render_pdf(simple_contact, tmpl)
        assert pdf[:4] == b"%PDF"

    def test_full_contact_pdf(self, renderer, full_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        pdf = renderer.render_pdf(full_contact, tmpl)
        assert len(pdf) > 1024

    def test_minimal_contact_pdf(self, renderer):
        """A contact with only a name should render without error."""
        tmpl = TemplateRegistry.get("claude-minimal")
        contact = Contact(name="Solo Name")
        pdf = renderer.render_pdf(contact, tmpl)
        assert pdf[:4] == b"%PDF"


# ---------------------------------------------------------------------------
# RenderService — Images
# ---------------------------------------------------------------------------

class TestRenderImage:
    def test_image_is_pil(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        img = renderer.render_image(simple_contact, tmpl, dpi=72)
        assert isinstance(img, Image.Image)

    def test_image_dimensions(self, low_dpi_spec, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        img = renderer.render_image(simple_contact, tmpl, dpi=72)
        # Width should match canvas width (card + 2×bleed) at 72 DPI
        expected_w = low_dpi_spec.canvas_width_px
        expected_h = low_dpi_spec.canvas_height_px
        assert img.width == expected_w
        assert img.height == expected_h

    def test_image_with_back(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        img = renderer.render_image(simple_contact, tmpl, dpi=72, include_back=True)
        # Combined front+back image should be twice as tall
        single = renderer.render_image(simple_contact, tmpl, dpi=72)
        assert img.height == single.height * 2

    def test_dark_template_image(self, renderer, simple_contact):
        tmpl = TemplateRegistry.get("claude-dark")
        img = renderer.render_image(simple_contact, tmpl, dpi=72)
        assert isinstance(img, Image.Image)


# ---------------------------------------------------------------------------
# ExportService
# ---------------------------------------------------------------------------

class TestExportService:
    def test_export_pdf_creates_file(self, exporter, renderer, simple_contact, tmp_path):
        tmpl = TemplateRegistry.get("claude-minimal")
        pdf = renderer.render_pdf(simple_contact, tmpl)
        path = exporter.export_pdf(pdf, simple_contact)
        assert path.exists()
        assert path.stat().st_size > 0
        assert path.suffix == ".pdf"

    def test_export_png_creates_file(self, exporter, renderer, simple_contact, tmp_path):
        tmpl = TemplateRegistry.get("claude-minimal")
        img = renderer.render_image(simple_contact, tmpl, dpi=72)
        path = exporter.export_png(img, simple_contact, dpi=72)
        assert path.exists()
        assert path.stat().st_size > 0
        assert path.suffix == ".png"

    def test_filename_convention(self, exporter, renderer, tmp_path):
        tmpl = TemplateRegistry.get("claude-minimal")
        contact = Contact(name="Jane Smith")
        pdf = renderer.render_pdf(contact, tmpl)
        path = exporter.export_pdf(pdf, contact)
        assert path.name == "smith_jane_businesscard.pdf"

    def test_generate_card_returns_paths(self, exporter, simple_contact):
        tmpl = TemplateRegistry.get("claude-minimal")
        paths = exporter.generate_card(simple_contact, tmpl, pdf=True, png=True)
        assert "pdf" in paths
        assert "png" in paths
        assert paths["pdf"].exists()
        assert paths["png"].exists()

    def test_generate_batch(self, exporter, tmp_path):
        tmpl = TemplateRegistry.get("claude-minimal")
        contacts = [
            Contact(name="Alice Foo", email="alice@example.com"),
            Contact(name="Bob Bar", email="bob@example.com"),
        ]
        results = exporter.generate_batch(contacts, tmpl, pdf=True)
        assert len(results) == 2
        for result in results:
            assert "pdf" in result
            assert result["pdf"].exists()

    def test_contact_sheet(self, exporter, tmp_path):
        tmpl = TemplateRegistry.get("claude-minimal")
        contacts = [
            Contact(name=f"Person {i}", email=f"p{i}@example.com")
            for i in range(4)
        ]
        path = exporter.generate_contact_sheet(contacts, tmpl, output_name="sheet.pdf")
        assert path.exists()
        assert path.stat().st_size > 0
        assert path.name == "sheet.pdf"


# ---------------------------------------------------------------------------
# Template registry
# ---------------------------------------------------------------------------

class TestTemplateRegistry:
    def test_get_claude_minimal(self):
        tmpl = TemplateRegistry.get("claude-minimal")
        assert tmpl.name == "claude-minimal"

    def test_get_claude_dark(self):
        tmpl = TemplateRegistry.get("claude-dark")
        assert tmpl.name == "claude-dark"

    def test_get_unknown_raises(self):
        with pytest.raises(KeyError, match="Unknown template"):
            TemplateRegistry.get("no-such-template")

    def test_list_templates(self):
        templates = TemplateRegistry.list_templates()
        names = [t.name for t in templates]
        assert "claude-minimal" in names
        assert "claude-dark" in names

    def test_names_sorted(self):
        names = TemplateRegistry.names()
        assert names == sorted(names)
