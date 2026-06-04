from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class InvoiceStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    OVERDUE = "OVERDUE"


class Address(BaseModel):
    street: str
    city: str
    pin_code: str


class LineItem(BaseModel):
    item_name: str
    quantity: int
    unit_price: float
    total_price: float


class Invoice(BaseModel):
    invoice_number: str
    invoice_date: str

    supplier_name: str
    customer_name: str

    total_amount: float

    status: InvoiceStatus

    billing_address: Address

    line_items: List[LineItem]

    notes: Optional[str] = None