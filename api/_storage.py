"""S3-compatible object storage — uploads PDF bytes and returns a public URL.

Works with AWS S3, Cloudflare R2, DigitalOcean Spaces, Backblaze B2, or any
S3-compatible provider. Configure via environment variables:

  S3_ACCESS_KEY_ID       Access key (required)
  S3_SECRET_ACCESS_KEY   Secret key (required)
  S3_BUCKET              Bucket name (required)
  S3_ENDPOINT_URL        Custom endpoint for non-AWS providers, e.g.
                           https://<account>.r2.cloudflarestorage.com  (R2)
                           https://nyc3.digitaloceanspaces.com          (DO)
                         Omit for standard AWS S3.
  S3_REGION              Region string; use "auto" for Cloudflare R2.
                         Defaults to "us-east-1".
  S3_PUBLIC_URL          Base URL of the publicly accessible bucket, e.g.
                           https://pub-<hash>.r2.dev  (R2 public bucket)
                           https://<bucket>.s3.amazonaws.com  (S3 static site)
                         When set, objects are returned as a plain public URL.
                         When omitted, a 7-day presigned URL is used instead.

Cloudprinter fetches the PDF when it processes the print job, so the URL must
remain accessible for at least several days. The 7-day presigned URL fallback
satisfies this for standard orders.
"""
from __future__ import annotations

import asyncio
import os

import boto3
from botocore.config import Config


def _upload_sync(pdf_bytes: bytes, key: str) -> str:
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
    """Upload PDF bytes to S3-compatible storage and return a public URL."""
    return await asyncio.to_thread(_upload_sync, pdf_bytes, pathname)
