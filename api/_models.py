"""Pydantic request/response models for the orders API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CardOrderRequest(BaseModel):
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    email: str
    signal: Optional[str] = None
    linkedin: Optional[str] = None
    quantity: int = Field(default=100, ge=50, le=200)

    @field_validator("email")
    @classmethod
    def email_must_be_tpo(cls, v: str) -> str:
        if not v.strip().lower().endswith("@tpo.group"):
            raise ValueError("Email must be a @tpo.group address")
        return v.strip()


class OrderResponse(BaseModel):
    reference: str
    status: str
    message: str
