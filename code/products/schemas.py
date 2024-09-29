from typing import Optional
from pydantic import BaseModel, condecimal, conint
from uuid import UUID


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: condecimal(gt=0)
    quantity_in_stock: conint(ge=0)


class ProductCreate(ProductBase):
    ...


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: condecimal(gt=0)
    quantity_in_stock: conint(ge=0)
