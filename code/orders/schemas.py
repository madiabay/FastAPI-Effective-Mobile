from datetime import datetime
from pydantic import BaseModel, conint
from uuid import UUID

from .constants import OrderStatus


class OrderBase(BaseModel):
    id: UUID
    created_at: datetime
    status: OrderStatus


class OrderItem(BaseModel):
    product_id: UUID
    quantity_in_order: conint(ge=0)


class OrderUpdate(BaseModel):
    status: OrderStatus
