import uuid
from datetime import datetime
from . import database
import ormar
from .constants import OrderStatus

ormar_base_config = ormar.OrmarConfig(
    database=database.database,
    metadata=database.metadata,
)
target_metadata = ormar_base_config.metadata


class Product(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id = ormar.UUID(primary_key=True, default=uuid.uuid4, index=True)
    name = ormar.String(max_length=255, index=True)
    description = ormar.Text(default=None)
    price = ormar.Decimal(max_digits=14, decimal_places=2)
    quantity_in_stock = ormar.Integer(nullable=False)


class Order(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id = ormar.UUID(primary_key=True, default=uuid.uuid4, index=True)
    created_at = ormar.DateTime(default=datetime.utcnow)
    status = ormar.Enum(enum_class=OrderStatus, default=OrderStatus.NEW)


class OrderItem(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id = ormar.UUID(primary_key=True, default=uuid.uuid4, index=True)
    order = ormar.ForeignKey(Order)
    product = ormar.ForeignKey(Product)
    quantity_in_order = ormar.Integer(nullable=False)
