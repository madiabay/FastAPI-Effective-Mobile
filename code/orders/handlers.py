import uuid
from typing import List

from fastapi import Response, status
from fastapi.responses import JSONResponse

from .services import OrderServiceV1
from .schemas import OrderItem, OrderUpdate
from code.meta import Order


class OrderHandler:
    order_services = OrderServiceV1()

    async def create_order(self, order_items: List[OrderItem], response: Response):
        created_order = await self.order_services.create_order(order_items=order_items)
        if isinstance(created_order, dict):
            return JSONResponse(content=created_order, status_code=status.HTTP_400_BAD_REQUEST)
        created_order = await created_order.load_all()
        response.status_code = status.HTTP_201_CREATED

        return created_order

    async def read_orders(self, response: Response) -> List[Order]:
        orders = await self.order_services.get_orders()
        response.status_code = status.HTTP_200_OK
        return orders

    async def read_order(self, order_id: uuid.UUID, response: Response) -> Order:
        product = await self.order_services.get_order(order_id)
        response.status_code = status.HTTP_200_OK
        return product

    async def update_order(self, order_id: uuid.UUID, order_status: OrderUpdate, response: Response) -> Order:
        updated_order = await self.order_services.update_order(order_id, order_status=order_status)
        response.status_code = status.HTTP_200_OK
        return updated_order
