"""Unit tests for the IngestService."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from bizcard.models.contact import Contact
from bizcard.services.ingest import IngestError, IngestService


@pytest.fixture
def ingest():
    return IngestService()


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# CSV ingestion
# ---------------------------------------------------------------------------

class TestCSVIngestion:
    def test_load_sample_csv(self, ingest, fixtures_dir):
        contacts = ingest.from_csv(fixtures_dir / "sample_contacts.csv")
        assert len(contacts) == 10
        assert all(isinstance(c, Contact) for c in contacts)

    def test_first_contact_fields(self, ingest, fixtures_dir):
        contacts = ingest.from_csv(fixtures_dir / "sample_contacts.csv")
        c = contacts[0]
        assert c.name == "Jane Smith"
        assert c.title == "Senior Engineer"
        assert c.company == "Acme Corp"
        assert c.email == "jane@acme.com"

    def test_missing_optional_fields(self, ingest, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("name,email\nJohn Doe,john@example.com\n")
        contacts = ingest.from_csv(csv_path)
        assert len(contacts) == 1
        assert contacts[0].phone is None

    def test_skip_invalid_rows(self, ingest, tmp_path):
        csv_path = tmp_path / "bad.csv"
        csv_path.write_text("name,email\n,invalid@\nValid Person,valid@example.com\n")
        # Empty name is invalid; second row should be loaded
        contacts = ingest.from_csv(csv_path, skip_errors=True)
        assert any(c.name == "Valid Person" for c in contacts)

    def test_file_not_found(self, ingest):
        with pytest.raises(IngestError):
            ingest.from_csv(Path("/nonexistent/file.csv"))

    def test_auto_detect_csv(self, ingest, fixtures_dir):
        contacts = ingest.from_file(fixtures_dir / "sample_contacts.csv")
        assert len(contacts) == 10


# ---------------------------------------------------------------------------
# JSON ingestion
# ---------------------------------------------------------------------------

class TestJSONIngestion:
    def test_load_array(self, ingest, tmp_path):
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "title": "Engineer"},
        ]
        path = tmp_path / "contacts.json"
        path.write_text(json.dumps(data))
        contacts = ingest.from_json(path)
        assert len(contacts) == 2
        assert contacts[0].email == "alice@example.com"

    def test_load_single_object(self, ingest, tmp_path):
        data = {"name": "Charlie", "company": "ACME"}
        path = tmp_path / "single.json"
        path.write_text(json.dumps(data))
        contacts = ingest.from_json(path)
        assert len(contacts) == 1
        assert contacts[0].company == "ACME"

    def test_malformed_json(self, ingest, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("{ bad json }")
        with pytest.raises(IngestError):
            ingest.from_json(path)

    def test_auto_detect_json(self, ingest, tmp_path):
        path = tmp_path / "contacts.json"
        path.write_text(json.dumps([{"name": "Dave"}]))
        contacts = ingest.from_file(path)
        assert len(contacts) == 1


# ---------------------------------------------------------------------------
# dict ingestion
# ---------------------------------------------------------------------------

class TestDictIngestion:
    def test_from_dict(self, ingest):
        c = ingest.from_dict({"name": "Eve", "email": "eve@example.com"})
        assert isinstance(c, Contact)
        assert c.name == "Eve"

    def test_from_dict_missing_name(self, ingest):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ingest.from_dict({"email": "no-name@example.com"})


# ---------------------------------------------------------------------------
# Unsupported format
# ---------------------------------------------------------------------------

class TestUnsupportedFormat:
    def test_unknown_extension(self, ingest, tmp_path):
        path = tmp_path / "contacts.xml"
        path.write_text("<root/>")
        with pytest.raises(IngestError, match="Unsupported"):
            ingest.from_file(path)
