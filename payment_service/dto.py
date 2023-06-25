from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PaymentDTO:
    id: int
    payment_url: str
    created_at: datetime
    paid_at: datetime
    status: StatusDTO


@dataclass
class StatusDTO:
    status: str


@dataclass
class InvoiceDTO:
    url: str
