from fastapi import APIRouter
from typing import List

from .handlers import ProductHandler
from code.meta import Product

product_handler = ProductHandler()
router = APIRouter(prefix='/products', tags=['products'])

router.add_api_route(
    '/',
    endpoint=product_handler.create_product,
    methods=['post'],
    response_model_exclude={'orderitems'},
)

router.add_api_route(
    '/',
    endpoint=product_handler.read_products,
    methods=['get'],
    response_model=List[Product],
    response_model_exclude_none=True,
)

router.add_api_route(
    '/{product_id}/',
    endpoint=product_handler.read_product,
    methods=['get'],
    response_model_exclude_none=True,
)

router.add_api_route(
    '/{pk}/',
    endpoint=product_handler.update_product,
    methods=['put'],
    response_model_exclude_none=True,
)

router.add_api_route(
    '/{pk}/',
    endpoint=product_handler.delete_product,
    methods=['delete'],
)
