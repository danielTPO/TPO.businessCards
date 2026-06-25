"""Vercel Blob storage — uploads PDF bytes and returns a permanent public URL.

Setup:
  1. Open your Vercel project dashboard → Storage → Create Database → Blob.
  2. Connect the store to your project.
  3. Copy BLOB_READ_WRITE_TOKEN from the store's "Tokens" tab into .env.

URLs returned by Vercel Blob are permanently public — no expiry, no presigning.
Cloudprinter can fetch the file at any point during the print job.
"""
from __future__ import annotations

import os

import httpx

_BLOB_API = "https://blob.vercel-storage.com"


async def upload_to_blob(pdf_bytes: bytes, pathname: str) -> str:
    """Upload PDF bytes to Vercel Blob and return the permanent public URL.

    Args:
        pdf_bytes: Raw PDF content.
        pathname: Object path inside the store, e.g. "bizcards/tpo-abc123.pdf".

    Returns:
        Permanent public HTTPS URL to the uploaded file.

    Raises:
        RuntimeError: If the Vercel Blob API returns a non-2xx response.
    """
    token = os.environ["BLOB_READ_WRITE_TOKEN"]

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{_BLOB_API}/{pathname}",
            content=pdf_bytes,
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-version": "7",
                "content-type": "application/pdf",
            },
            timeout=30.0,
        )

    if not resp.is_success:
        raise RuntimeError(f"Vercel Blob {resp.status_code}: {resp.text}")

    return resp.json()["url"]
