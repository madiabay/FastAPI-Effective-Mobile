import uuid
from typing import List

from fastapi import Response, status

from .services import ProductServiceV1
from .schemas import ProductCreate, ProductUpdate
from code.meta import Product


class ProductHandler:
    product_services = ProductServiceV1()

    async def create_product(self, product: ProductCreate, response: Response) -> Product:
        created_user = await self.product_services.create_product(product_dict=product.dict())
        response.status_code = status.HTTP_201_CREATED
        return created_user

    async def read_products(self, response: Response) -> List[Product]:
        products = await self.product_services.read_products()
        response.status_code = status.HTTP_200_OK
        return products

    async def read_product(self, product_id: uuid.UUID, response: Response) -> Product:
        product = await self.product_services.read_product(product_id)
        response.status_code = status.HTTP_200_OK
        return product

    async def update_product(self, product_id: uuid.UUID, product_data: ProductUpdate, response: Response) -> Product:
        product = await self.product_services.update_product(product_id, product_dict=product_data)
        response.status_code = status.HTTP_200_OK
        return product

    async def delete_product(self, product_id: uuid.UUID) -> Response:
        await self.product_services.delete_product(product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
