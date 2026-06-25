"""Cloudprinter CloudCore 1.0 API client."""
from __future__ import annotations

import json
import os
from typing import Optional

import httpx

_BASE = "https://api.cloudprinter.com/cloudcore/1.0"

_DELIVERY_ADDRESS = {
    "type": "delivery",
    "company": "TPO Group",
    "street1": "5 Moulton St, 6th FL",
    "zip": "04101",
    "city": "Portland",
    "state": "ME",
    "country": "US",
}


class CloudprinterError(Exception):
    """Raised when Cloudprinter returns a non-2xx response."""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        # Try to pretty-print JSON bodies for readability
        try:
            parsed = json.loads(body)
            self.body = json.dumps(parsed, indent=2)
        except Exception:
            pass
        super().__init__(f"HTTP {status_code}")


def _item_options(quantity: int) -> list[dict]:
    return [
        {"option_reference": "paper_350ecb", "count": str(quantity)},
        {"option_reference": "product_finish_matte", "count": "1"},
        {"option_reference": "right_angled_corners", "count": "1"},
    ]


async def _fetch_quote(
    client: httpx.AsyncClient,
    apikey: str,
    quantity: int,
) -> Optional[str]:
    payload = {
        "apikey": apikey,
        "country": "US",
        "items": [{
            "reference": "item-001",
            "product": "businesscard_ds_70x30_mm_bc_fc",
            "count": quantity,
            "options": _item_options(quantity),
        }],
    }
    try:
        resp = await client.post(f"{_BASE}/quotes/add", json=payload, timeout=15.0)
        resp.raise_for_status()
        body = resp.json()
        return body.get("hash") or body.get("quote")
    except Exception:
        return None


async def submit_order(
    *,
    reference: str,
    quantity: int,
    file_url: str,
    file_md5: str,
    notification_email: str,
) -> dict:
    """Submit a business card order to Cloudprinter CloudCore 1.0.

    Raises:
        CloudprinterError: Non-2xx response from Cloudprinter (includes status code + body).
    """
    apikey = os.environ["CLOUDPRINTER_API_KEY"]

    async with httpx.AsyncClient() as client:
        quote_hash = await _fetch_quote(client, apikey, quantity)

        address = dict(_DELIVERY_ADDRESS)
        address["email"] = notification_email

        payload: dict = {
            "apikey": apikey,
            "reference": reference,
            "email": notification_email,
            "shipping_level": "cp_saver",
            "addresses": [address],
            "items": [{
                "reference": f"{reference}-item",
                "product": "businesscard_ds_70x30_mm_bc_fc",
                "count": quantity,
                "files": [{
                    "type": "content",
                    "url": file_url,
                    "md5sum": file_md5,
                }],
                "options": _item_options(quantity),
            }],
        }

        if quote_hash:
            payload["quote"] = quote_hash

        resp = await client.post(f"{_BASE}/orders/add", json=payload, timeout=30.0)

        if not resp.is_success:
            raise CloudprinterError(resp.status_code, resp.text)

        return resp.json()
