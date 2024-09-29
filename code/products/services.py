import uuid
from typing import List
from fastapi import HTTPException, status
from .schemas import ProductUpdate
from code.meta import Product
from ormar.exceptions import NoMatch


class ProductServiceV1:

    @staticmethod
    async def create_product(product_dict: dict) -> Product:
        return await Product.objects.create(**product_dict)

    @staticmethod
    async def read_products() -> List[Product]:
        return await Product.objects.all()

    @staticmethod
    async def read_product(product_id: uuid.UUID) -> Product:
        try:
            product = await Product.objects.get(id=product_id)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        else:
            return product

    @staticmethod
    async def update_product(product_id: uuid.UUID, product_dict: ProductUpdate) -> Product:
        await Product.objects.filter(id=product_id).update(**product_dict.dict())

        try:
            product = await Product.objects.get(id=product_id)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        else:
            return product

    @staticmethod
    async def delete_product(product_id: uuid.UUID) -> None:
        try:
            product = await Product.objects.get(id=product_id)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        else:
            await product.delete()
