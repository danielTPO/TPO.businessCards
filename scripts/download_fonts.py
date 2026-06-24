#!/usr/bin/env python3
"""Download the Inter font family into bizcard/assets/fonts/.

Run this once after cloning the repository::

    python scripts/download_fonts.py

Requires: requests (``pip install requests``).

Font source: https://github.com/rsms/inter (SIL Open Font Licence 1.1)
"""

from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

ASSETS_FONTS = Path(__file__).parent.parent / "bizcard" / "assets" / "fonts"
INTER_RELEASE_URL = (
    "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"
)

WANTED_FILES = {
    "Inter Desktop/Inter-Regular.ttf",
    "Inter Desktop/Inter-Medium.ttf",
    "Inter Desktop/Inter-Bold.ttf",
    "Inter Desktop/Inter-Light.ttf",
    "Inter Desktop/Inter-SemiBold.ttf",
}


def download_inter() -> None:
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' is not installed.  Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    ASSETS_FONTS.mkdir(parents=True, exist_ok=True)

    print(f"Downloading Inter font from {INTER_RELEASE_URL} …")
    resp = requests.get(INTER_RELEASE_URL, stream=True, timeout=60)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    chunks = []
    for chunk in resp.iter_content(chunk_size=65536):
        chunks.append(chunk)
        downloaded += len(chunk)
        if total:
            pct = downloaded / total * 100
            print(f"\r  {pct:.1f}%", end="", flush=True)
    print()

    zip_data = b"".join(chunks)
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        for member in zf.namelist():
            # Normalise path separators for cross-platform matching
            normalised = member.replace("\\", "/")
            for wanted in WANTED_FILES:
                if normalised.endswith(wanted.split("/")[-1]) and (
                    "Desktop" in normalised or "Variable" not in normalised
                ):
                    dest = ASSETS_FONTS / Path(wanted).name
                    dest.write_bytes(zf.read(member))
                    print(f"  ✓  {dest.name}")
                    break

    print(f"\nFonts installed to {ASSETS_FONTS}")


if __name__ == "__main__":
    download_inter()
