"""POST /api/orders — Vercel Python serverless function.

Handles the full order flow:
  1. Validate the request
  2. Generate a PDF in memory via the bizcard package
  3. Upload to Vercel Blob (permanent public URL)
  4. Submit to Cloudprinter CloudCore 1.0
  5. Append to output/orders.jsonl

Vercel invokes the `handler` variable (a Mangum ASGI adapter wrapping the FastAPI app).
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root and api/ are both importable regardless of Vercel's cwd
_root = Path(__file__).parent.parent
_api = Path(__file__).parent
for _p in (str(_root), str(_api)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dotenv import load_dotenv
load_dotenv(_root / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from _models import CardOrderRequest, OrderResponse
from _cloudprinter import submit_order
from _generator import generate_pdf_bytes
from _storage import upload_to_blob

app = FastAPI(title="TPO Business Card Ordering", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_LOG_PATH = _root / "output" / "orders.jsonl"


@app.post("/api/orders", response_model=OrderResponse)
async def create_order(req: CardOrderRequest) -> OrderResponse:
    order_ref = f"tpo-{uuid.uuid4().hex[:12]}"
    notification_email = os.environ.get("ORDER_NOTIFICATION_EMAIL", req.email)

    # 1. Generate PDF in memory
    try:
        pdf_bytes, md5 = generate_pdf_bytes(req)
    except Exception as exc:
        _log(order_ref, req, "failed", f"PDF generation: {exc}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {exc}")

    # 2. Upload to Vercel Blob
    try:
        file_url = await upload_to_blob(pdf_bytes, f"bizcards/{order_ref}.pdf")
    except Exception as exc:
        _log(order_ref, req, "failed", f"Blob upload: {exc}")
        raise HTTPException(status_code=502, detail=f"Storage upload failed: {exc}")

    # 3. Submit to Cloudprinter
    try:
        cp_response = await submit_order(
            reference=order_ref,
            quantity=req.quantity,
            file_url=file_url,
            file_md5=md5,
            notification_email=notification_email,
        )
    except Exception as exc:
        _log(order_ref, req, "failed", f"Cloudprinter: {exc}")
        raise HTTPException(status_code=502, detail=f"Cloudprinter submission failed: {exc}")

    _log(order_ref, req, "submitted", cp_response)

    return OrderResponse(
        reference=order_ref,
        status="submitted",
        message=f"Order {order_ref} submitted to Cloudprinter.",
    )


def _log(reference: str, req: CardOrderRequest, status: str, detail: object) -> None:
    try:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "reference": reference,
            "name": req.name,
            "email": req.email,
            "quantity": req.quantity,
            "status": status,
            "detail": detail if isinstance(detail, str) else str(detail),
        }
        with _LOG_PATH.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


# Vercel invokes this as the ASGI handler
handler = Mangum(app, lifespan="off")
