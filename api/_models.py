"""Pydantic request/response models for the orders API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CardOrderRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=30)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    signal: Optional[str] = Field(default=None, max_length=60)
    linkedin: Optional[str] = Field(default=None, max_length=300)
    quantity: int = Field(default=250, ge=50, le=5000)


class OrderResponse(BaseModel):
    reference: str
    status: str
    message: str
