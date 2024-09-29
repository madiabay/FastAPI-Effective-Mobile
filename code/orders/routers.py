from fastapi import APIRouter
from typing import List

from .handlers import OrderHandler
from code.meta import Order

order_handler = OrderHandler()
router = APIRouter(prefix='/orders', tags=['orders'])

router.add_api_route(
    '/',
    endpoint=order_handler.create_order,
    methods=['post'],
    response_model_exclude={'orderitems__product'},
    response_model_exclude_unset=True,
)

router.add_api_route(
    '/',
    endpoint=order_handler.read_orders,
    methods=['get'],
    response_model=List[Order],
    response_model_exclude={'status'},
    response_model_exclude_none=True,
)

router.add_api_route(
    '/{product_id}/',
    endpoint=order_handler.read_order,
    methods=['get'],
    response_model_exclude_none=True,
)

router.add_api_route(
    '/{pk}/',
    endpoint=order_handler.update_order,
    methods=['patch'],
    response_model_exclude_none=True,
)
