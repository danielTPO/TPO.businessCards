#!/usr/bin/env python3
"""Download fonts into bizcard/assets/fonts/.

Downloads two families:

  Inter        — primary sans-serif (SIL OFL 1.1)
                 https://github.com/rsms/inter
  Libre Baskerville — open-source serif for the anthropic-* templates (OFL 1.1)
                 https://fonts.google.com/specimen/Libre+Baskerville

Tiempos Text (used by Anthropic) is a proprietary typeface sold by Klim Type
Foundry.  If you have a licence, place TiemposText-Bold.ttf and
TiemposText-Regular.ttf into bizcard/assets/fonts/ manually.  The templates
fall back to Times-Roman (PDF) and Libre Baskerville (PNG) when the files are
absent.

Run once after cloning::

    pip install requests
    python scripts/download_fonts.py
"""

from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

ASSETS_FONTS = Path(__file__).parent.parent / "bizcard" / "assets" / "fonts"

INTER_URL = "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"
INTER_WANTED = {
    "Inter Desktop/Inter-Regular.ttf",
    "Inter Desktop/Inter-Medium.ttf",
    "Inter Desktop/Inter-Bold.ttf",
    "Inter Desktop/Inter-Light.ttf",
    "Inter Desktop/Inter-SemiBold.ttf",
}

# Google Fonts static download for Libre Baskerville
BASKERVILLE_FILES = {
    "LibreBaskerville-Regular.ttf": (
        "https://fonts.gstatic.com/s/librebaskerville/v14/"
        "kmKnZrc3Hgbbcjq75U4uslyuy4kn0qviTjYwI8Gcw6Oi.ttf"
    ),
    "LibreBaskerville-Bold.ttf": (
        "https://fonts.gstatic.com/s/librebaskerville/v14/"
        "kmKiZrc3Hgbbcjq75U4uslyuy4kn0ptiTjYwI8Gcw6Oi.ttf"
    ),
}


def _fetch(url: str, label: str, requests_mod: object) -> bytes:
    print(f"Downloading {label} …")
    resp = requests_mod.get(url, stream=True, timeout=90)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    chunks = []
    done = 0
    for chunk in resp.iter_content(chunk_size=65536):
        chunks.append(chunk)
        done += len(chunk)
        if total:
            print(f"\r  {done / total * 100:.1f}%", end="", flush=True)
    print()
    return b"".join(chunks)


def download_inter(requests_mod: object) -> None:
    data = _fetch(INTER_URL, "Inter font family", requests_mod)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for member in zf.namelist():
            norm = member.replace("\\", "/")
            for wanted in INTER_WANTED:
                if norm.endswith(wanted.split("/")[-1]) and (
                    "Desktop" in norm or "Variable" not in norm
                ):
                    dest = ASSETS_FONTS / Path(wanted).name
                    dest.write_bytes(zf.read(member))
                    print(f"  ✓  {dest.name}")
                    break


def download_libre_baskerville(requests_mod: object) -> None:
    for filename, url in BASKERVILLE_FILES.items():
        dest = ASSETS_FONTS / filename
        data = _fetch(url, filename, requests_mod)
        dest.write_bytes(data)
        print(f"  ✓  {dest.name}")


def main() -> None:
    try:
        import requests
    except ImportError:
        print("ERROR: requests not installed.  Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    ASSETS_FONTS.mkdir(parents=True, exist_ok=True)

    download_inter(requests)
    download_libre_baskerville(requests)

    print(f"\nAll fonts installed to {ASSETS_FONTS}")
    print()
    print("NOTE: Tiempos Text (used by Anthropic) is proprietary.")
    print("      To use it, place TiemposText-Bold.ttf and TiemposText-Regular.ttf")
    print("      into bizcard/assets/fonts/ manually.")
    print("      Without it, the anthropic-* templates use Libre Baskerville.")


if __name__ == "__main__":
    main()
