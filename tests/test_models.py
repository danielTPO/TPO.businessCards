"""Unit tests for Contact and CardSpec models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from bizcard.models.contact import Contact
from bizcard.models.card import CardSpec, Orientation


# ---------------------------------------------------------------------------
# Contact model
# ---------------------------------------------------------------------------

class TestContactCreation:
    def test_minimal_contact(self):
        c = Contact(name="Jane Smith")
        assert c.name == "Jane Smith"
        assert c.email is None
        assert c.phone is None

    def test_full_contact(self):
        c = Contact(
            name="Jane Smith",
            title="Senior Engineer",
            company="Acme Corp",
            email="Jane@ACME.COM",
            phone="+1 555 000 1234",
            website="https://acme.com/",
            linkedin="https://linkedin.com/in/janesmith",
        )
        assert c.name == "Jane Smith"
        assert c.email == "jane@acme.com"  # normalised to lowercase
        assert c.website == "acme.com"      # protocol stripped, trailing slash removed
        assert c.linkedin == "in/janesmith"  # normalised

    def test_name_required(self):
        with pytest.raises(ValidationError):
            Contact(name="")

    def test_empty_optional_fields_become_none(self):
        c = Contact(name="Jane", title="", company="  ", email="")
        assert c.title is None
        assert c.company is None
        assert c.email is None

    def test_whitespace_name_collapsed(self):
        c = Contact(name="  Jane   Smith  ")
        assert c.name == "Jane Smith"


class TestContactProperties:
    @pytest.fixture
    def contact(self):
        return Contact(name="Jane Marie Smith", email="jane@example.com")

    def test_first_name(self, contact):
        assert contact.first_name == "Jane"

    def test_last_name(self, contact):
        assert contact.last_name == "Marie Smith"

    def test_initials(self, contact):
        assert contact.initials == "JS"

    def test_initials_single_name(self):
        c = Contact(name="Madonna")
        assert c.initials == "M"

    def test_output_filename_stem(self, contact):
        assert contact.output_filename_stem == "smith_jane"

    def test_contact_fields_ordering(self):
        c = Contact(
            name="X",
            company="Corp",
            email="x@x.com",
            phone="555",
            website="x.com",
            linkedin="in/x",
        )
        keys = [k for k, _ in c.contact_fields]
        assert keys == ["company", "email", "phone", "web", "linkedin"]

    def test_contact_fields_empty(self):
        c = Contact(name="No Details")
        assert c.contact_fields == []


class TestContactNormalisation:
    def test_linkedin_full_url(self):
        c = Contact(name="X", linkedin="https://www.linkedin.com/in/janesmith/")
        assert c.linkedin == "in/janesmith"

    def test_linkedin_bare_handle(self):
        c = Contact(name="X", linkedin="janesmith")
        assert c.linkedin == "in/janesmith"

    def test_linkedin_already_normalised(self):
        c = Contact(name="X", linkedin="in/janesmith")
        assert c.linkedin == "in/janesmith"

    def test_website_strips_protocol(self):
        c = Contact(name="X", website="https://www.example.com/")
        assert c.website == "www.example.com"

    def test_phone_strips_invalid_chars(self):
        c = Contact(name="X", phone="+1 (555) 000-1234")
        # Should preserve common phone chars
        assert "555" in c.phone
        assert "000" in c.phone


# ---------------------------------------------------------------------------
# CardSpec model
# ---------------------------------------------------------------------------

class TestCardSpec:
    def test_standard_landscape(self):
        spec = CardSpec.standard_landscape()
        assert spec.width_in == 3.5
        assert spec.height_in == 2.0
        assert spec.orientation == Orientation.LANDSCAPE

    def test_standard_portrait(self):
        spec = CardSpec.standard_portrait()
        assert spec.width_in == 2.0
        assert spec.height_in == 3.5
        assert spec.orientation == Orientation.PORTRAIT

    def test_point_conversion(self):
        spec = CardSpec(width_in=3.5, height_in=2.0, dpi=300)
        assert abs(spec.width_pt - 252.0) < 0.01
        assert abs(spec.height_pt - 144.0) < 0.01

    def test_pixel_conversion(self):
        spec = CardSpec(width_in=3.5, height_in=2.0, dpi=300)
        assert spec.width_px == 1050
        assert spec.height_px == 600

    def test_canvas_includes_bleed(self):
        spec = CardSpec(width_in=3.5, height_in=2.0, bleed_in=0.125, dpi=300)
        assert spec.canvas_width_px == 1050 + 2 * 38  # 38 ≈ 0.125 * 300
        assert spec.canvas_height_px == 600 + 2 * 38

    def test_pt_to_px_roundtrip(self):
        spec = CardSpec(dpi=300)
        pt = 72.0  # 1 inch
        px = spec.pt_to_px(pt)
        assert px == 300  # 1 inch at 300 DPI

    def test_portrait_auto_swap(self):
        # If user specifies landscape dims but portrait orientation, dims should swap
        spec = CardSpec(width_in=3.5, height_in=2.0, orientation=Orientation.PORTRAIT)
        assert spec.width_in < spec.height_in
