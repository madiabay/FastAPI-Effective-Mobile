import uuid
from typing import List
from fastapi import HTTPException, status
from .schemas import OrderItem, OrderUpdate
from code.meta import Order, OrderItem, Product
from ormar.exceptions import NoMatch
from code.database import database


class OrderServiceV1:

    @staticmethod
    async def create_order(order_items: List[OrderItem]):
        async with database.transaction():
            created_order = await Order.objects.create()
            order_items_for_creation = []

            for item in order_items:
                try:
                    product = await Product.objects.get(id=item.product_id)
                except NoMatch:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product with {item.product_id} ID not found"
                    )
                else:
                    if product.quantity_in_stock < item.quantity_in_order:
                        msg = f"Недостаточно товара на складе для продукта {product.name}."
                        return {'message': msg}
                    product.quantity_in_stock -= item.quantity_in_order
                    await product.update()
                    order_items_for_creation.append(
                        OrderItem(
                            order=created_order,
                            product=product,
                            quantity_in_order=item.quantity_in_order,
                        )
                    )

            await OrderItem.objects.bulk_create(order_items_for_creation)

            return created_order

    @staticmethod
    async def get_orders() -> List[Order]:
        return await Order.objects.prefetch_related('orderitems').all()

    @staticmethod
    async def get_order(order_id: uuid.UUID) -> Order:
        try:
            order = await Order.objects.prefetch_related('orderitems').fields({
                'id',
                'created_at',
                'status',
            }).get(id=order_id)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        else:
            return order

    @staticmethod
    async def update_order(order_id: uuid.UUID, order_status: OrderUpdate) -> Order:
        try:
            order = await Order.objects.get(id=order_id)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        else:
            await order.update(status=order_status.status.value)
            return order
