"""Object storage — uploads PDF bytes and returns a public URL.

Supports two modes:
  1. Local filesystem (for testing/dev) — configure LOCAL_STORAGE_DIR
  2. S3-compatible (for production) — configure S3_* variables

LOCAL STORAGE (Testing)
  LOCAL_STORAGE_DIR      Directory to store PDFs, e.g. /tmp/bizcards
                         When set, files are served from this local directory.
                         Overrides S3 configuration.

S3-COMPATIBLE STORAGE (Production)
  S3_ACCESS_KEY_ID       Access key (required for S3)
  S3_SECRET_ACCESS_KEY   Secret key (required for S3)
  S3_BUCKET              Bucket name (required for S3)
  S3_ENDPOINT_URL        Custom endpoint for non-AWS providers, e.g.
                           https://<account_id>.r2.cloudflarestorage.com  (R2)
                           https://nyc3.digitaloceanspaces.com            (DO)
                         Omit for standard AWS S3.
  S3_REGION              Region string; use "auto" for Cloudflare R2.
                         Defaults to "us-east-1".
  S3_PUBLIC_URL          Base URL of the publicly accessible bucket, e.g.
                           https://pub-<hash>.r2.dev  (R2 public bucket)
                           https://<bucket>.s3.amazonaws.com  (S3 static site)
                         When set, objects are returned as a plain public URL.
                         When omitted, a 7-day presigned URL is used instead.
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

import boto3
from botocore.config import Config


def _upload_local(pdf_bytes: bytes, key: str) -> str:
    """Upload to local filesystem and return a file URL."""
    storage_dir = Path(os.environ["LOCAL_STORAGE_DIR"])
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = storage_dir / key
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(pdf_bytes)
    
    return f"file://{filepath.absolute()}"


def _upload_s3(pdf_bytes: bytes, key: str) -> str:
    """Upload to S3-compatible storage and return a public URL."""
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("S3_ENDPOINT_URL") or None,
        aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
        region_name=os.environ.get("S3_REGION", "us-east-1"),
        config=Config(signature_version="s3v4"),
    )
    bucket = os.environ["S3_BUCKET"]

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=pdf_bytes,
        ContentType="application/pdf",
    )

    public_base = os.environ.get("S3_PUBLIC_URL", "").rstrip("/")
    if public_base:
        return f"{public_base}/{key}"

    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=7 * 24 * 3600,
    )


async def upload_to_blob(pdf_bytes: bytes, pathname: str) -> str:
    """Upload PDF bytes to storage and return a public URL.
    
    Uses local filesystem if LOCAL_STORAGE_DIR is set, otherwise uses S3.
    """
    if os.environ.get("LOCAL_STORAGE_DIR"):
        return await asyncio.to_thread(_upload_local, pdf_bytes, pathname)
    return await asyncio.to_thread(_upload_s3, pdf_bytes, pathname)
