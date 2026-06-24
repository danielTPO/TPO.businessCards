"""Data ingestion service.

Supports loading contact records from:
- CSV files (one contact per row)
- JSON files (array of objects or single object)
- vCard (.vcf) files (single or multi-card)
- Python dicts (programmatic API)
- CLI argument dicts

All ingestion paths produce validated :class:`~bizcard.models.contact.Contact`
objects.  Validation errors are collected and logged rather than aborting the
entire batch, so a single bad row does not prevent the rest from rendering.
"""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Any, Iterator

from pydantic import ValidationError

from bizcard.models.contact import Contact

log = logging.getLogger(__name__)


class IngestError(Exception):
    """Raised when a file cannot be parsed at all (format-level failure)."""


class IngestService:
    """Multi-format contact data loader.

    Example::

        service = IngestService()
        contacts = service.from_csv(Path("contacts.csv"))
        contacts = service.from_json(Path("contacts.json"))
        contacts = service.from_dict({"name": "Jane Smith", "email": "j@example.com"})
    """

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def from_dict(self, data: dict[str, Any]) -> Contact:
        """Create a single :class:`Contact` from a plain dictionary.

        Args:
            data: Dict with keys matching Contact field names.

        Returns:
            Validated :class:`Contact` instance.

        Raises:
            ValidationError: If required fields are missing or values are invalid.
        """
        return Contact(**data)

    def from_csv(self, path: Path, *, skip_errors: bool = True) -> list[Contact]:
        """Load all rows from a CSV file.

        The first row must be a header row with field names matching
        :class:`Contact` attributes.  Unrecognised columns are silently
        ignored.  Empty rows are skipped.

        Args:
            path: Path to the CSV file.
            skip_errors: If ``True``, log validation errors and continue.
                If ``False``, re-raise on the first error.

        Returns:
            List of validated :class:`Contact` instances.

        Raises:
            IngestError: If the file cannot be read or parsed.
        """
        contacts: list[Contact] = []
        try:
            with path.open(newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh)
                for i, row in enumerate(reader, start=2):  # row 1 is header
                    row = {k.strip().lower(): v.strip() for k, v in row.items() if k}
                    try:
                        contacts.append(Contact(**row))
                    except (ValidationError, TypeError) as exc:
                        msg = f"CSV row {i}: {exc}"
                        if skip_errors:
                            log.warning(msg)
                        else:
                            raise IngestError(msg) from exc
        except OSError as exc:
            raise IngestError(f"Cannot read CSV '{path}': {exc}") from exc
        except csv.Error as exc:
            raise IngestError(f"CSV parse error in '{path}': {exc}") from exc
        log.info("Loaded %d contact(s) from %s", len(contacts), path)
        return contacts

    def from_json(self, path: Path, *, skip_errors: bool = True) -> list[Contact]:
        """Load contacts from a JSON file.

        The file must contain either a JSON array of objects or a single
        object.

        Args:
            path: Path to the JSON file.
            skip_errors: If ``True``, log validation errors and continue.

        Returns:
            List of validated :class:`Contact` instances.

        Raises:
            IngestError: If the file cannot be read or the JSON is malformed.
        """
        try:
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except OSError as exc:
            raise IngestError(f"Cannot read JSON '{path}': {exc}") from exc
        except json.JSONDecodeError as exc:
            raise IngestError(f"JSON parse error in '{path}': {exc}") from exc

        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            raise IngestError(f"JSON '{path}' must be an array or a single object")

        contacts: list[Contact] = []
        for i, record in enumerate(data):
            try:
                contacts.append(Contact(**record))
            except (ValidationError, TypeError) as exc:
                msg = f"JSON record {i}: {exc}"
                if skip_errors:
                    log.warning(msg)
                else:
                    raise IngestError(msg) from exc
        log.info("Loaded %d contact(s) from %s", len(contacts), path)
        return contacts

    def from_vcf(self, path: Path, *, skip_errors: bool = True) -> list[Contact]:
        """Load contacts from a vCard (.vcf) file.

        Requires the ``vobject`` library.  Supports both single-card and
        multi-card files.

        Args:
            path: Path to the .vcf file.
            skip_errors: If ``True``, log errors and continue to the next vCard.

        Returns:
            List of validated :class:`Contact` instances.

        Raises:
            IngestError: If the file cannot be read.
        """
        try:
            import vobject  # type: ignore[import]
        except ImportError as exc:
            raise IngestError(
                "vobject library is required for vCard import: pip install vobject"
            ) from exc

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise IngestError(f"Cannot read vCard '{path}': {exc}") from exc

        contacts: list[Contact] = []
        for vcard in vobject.readComponents(text):
            try:
                data = _vcard_to_dict(vcard)
                contacts.append(Contact(**data))
            except Exception as exc:  # noqa: BLE001
                msg = f"vCard parse error: {exc}"
                if skip_errors:
                    log.warning(msg)
                else:
                    raise IngestError(msg) from exc

        log.info("Loaded %d contact(s) from %s", len(contacts), path)
        return contacts

    def from_file(self, path: Path, *, skip_errors: bool = True) -> list[Contact]:
        """Auto-detect format from extension and delegate to the right loader.

        Supported extensions: ``.csv``, ``.json``, ``.vcf``, ``.vcard``.

        Args:
            path: Path to the input file.
            skip_errors: Forwarded to the underlying loader.

        Returns:
            List of validated :class:`Contact` instances.

        Raises:
            IngestError: If the file format is unrecognised.
        """
        suffix = path.suffix.lower()
        if suffix == ".csv":
            return self.from_csv(path, skip_errors=skip_errors)
        if suffix == ".json":
            return self.from_json(path, skip_errors=skip_errors)
        if suffix in (".vcf", ".vcard"):
            return self.from_vcf(path, skip_errors=skip_errors)
        raise IngestError(
            f"Unsupported file format '{suffix}'. Supported: .csv, .json, .vcf, .vcard"
        )


# ---------------------------------------------------------------------------
# vCard conversion helper
# ---------------------------------------------------------------------------

def _vcard_to_dict(vcard: object) -> dict[str, str]:
    """Extract a flat dict from a ``vobject`` vCard component."""
    data: dict[str, str] = {}

    def _get(attr: str) -> str:
        try:
            return getattr(vcard, attr).value
        except AttributeError:
            return ""

    fn = _get("fn")
    if fn:
        data["name"] = fn

    org = _get("org")
    if isinstance(org, (list, tuple)):
        org = " ".join(str(p) for p in org if p)
    if org:
        data["company"] = str(org)

    title = _get("title")
    if title:
        data["title"] = title

    try:
        for email in vcard.contents.get("email", []):
            data["email"] = email.value
            break
    except AttributeError:
        pass

    try:
        for tel in vcard.contents.get("tel", []):
            data["phone"] = tel.value
            break
    except AttributeError:
        pass

    try:
        for url in vcard.contents.get("url", []):
            data["website"] = url.value
            break
    except AttributeError:
        pass

    return data
